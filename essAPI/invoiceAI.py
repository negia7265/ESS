import genie # a custom set of functions made to extract date,distance & address
import tensorflow as tf # used for deep learning 
import pandas as pd # Most important to build dataframes used as dataset or input to ml model
import pdfplumber # best reliable open source project to parse pdf 
from generator import generate_amount_candidates
import os
import re
import cv2
import pytesseract
import numpy as np
from PIL import Image
from invoice_dateparser import get_date
from distance_parser import get_distance
current_directory = os.getcwd()

# Relative path to the model file
relative_path = 'essAPI/amount_model_tf.h5'

# Combine the current directory and the relative path
model_path = os.path.join(current_directory, relative_path)
# model_path='./amount_model_tf.h5' #linux path
model=tf.keras.models.load_model(model_path)
# This class receives either an invoice pdf or image ,
# information extraction from unstructured invoice is done to extract date,
# distance, amount and address.
relative_path_eng = "essAPI"
absolute_path = os.path.abspath(relative_path_eng)
# absolute_path=os.getcwd() #linux 
class InvoiceParser:
    def __init__(self,invoice_data,invoice_data_type):
        self.date=''
        self.distance=''
        self.amount=''
        self.src=''
        self.dest=''
        self.highest_probability=None
        self.total_amount=None
        self.address=[]
        if invoice_data_type=='pdf':
            invoice = pdfplumber.open(invoice_data)
            text_arr=[]
            for page in invoice.pages:
                # dedupe chars is a method which removes overlapped lines in a page
                # bold fonts can be considered double /overlapped lines so it is used here.  
                page=page.dedupe_chars(tolerance=1)
                text=page.extract_text()
                text_arr.append(text)
                tax_invoice_page='tax invoice' in text.lower()
                # convert invoice page to image with 300 DPI image quality , black and white color.
                image=page.to_image(resolution=300).original
                preprocessed_img=genie.preprocess_img(image)
                # The text positional features along with text itself is extracted from 
                # pdf to feed as input to ml model.
                if page.page_number==1: #assuming amount occurs on first page of invoice
                    df=pytesseract.image_to_data(preprocessed_img,lang='eng',config=f'--tessdata-dir "{absolute_path}"', output_type='data.frame')
                    height=max(df['top'].max(),df['height'].max())
                    width=max(df['left'].max(),df['width'].max())
                    self.extract_amount(df,height,width)
                image=np.array(image.convert('L')) #black and white image
                if len(self.address)<2:
                    for addr in genie.get_address(image,preprocessed_img):
                        self.address.append(addr)
                        if len(self.address)==2:
                            break
            self.date=get_date(text_arr)
            self.distance=get_distance(text_arr)
            invoice.close()
        else:  
            image=Image.open(invoice_data)
            preprocessed_img=genie.preprocess_img(image) 
            text = pytesseract.image_to_string(preprocessed_img, lang='eng')
            self.date=get_date([text])
            self.distance=get_distance([text])
            # dataframe contains positional features of each word present in invoice.
            df=pytesseract.image_to_data(preprocessed_img,lang='eng',config=f'--tessdata-dir "{absolute_path}"', output_type='data.frame')
            height=max(df['top'].max(),df['height'].max())
            width=max(df['left'].max(),df['width'].max())
            if not df.empty:
            # Tesseract ocr provides image dimensions in it's dataframe 
               self.extract_amount(df,height,width)

            image=cv2.imread('300_dpi.jpg')
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            for addr in genie.get_address(image,preprocessed_img):
               self.address.append(addr)
               if len(self.address)==2:
                    break
                                                           
    def extract_amount(self,data,height,width):
        #Height and width are dimensions of invoice
        # amounts are extracted such as tax, subtotal, due, total amount these are known candidates
        df=generate_amount_candidates(data,10,'-1',height,width)    #model is trained with 10 number of neighbours    
        df.reset_index(inplace=True)
        cand_pos=tf.constant(list(df['candidate_position']))
        neighbours=tf.constant(list(df['neighbour_id']))
        neighbour_positions=tf.constant(list(df['neighbour_relative_position']))
        field_id=tf.constant(list(df['field_id']))
        # if the number of candidates is null then there is no need to proceed further with empty data
        if len(df['field_id'])==0:
            return None
        prediction=model.predict((field_id,cand_pos,neighbours,neighbour_positions))
        # for each prediction select the amounts with their probability of being total amount
        length=len(prediction)
        for index in range(length):
           amount=float(df.at[index,'text']) 
           probability=float(prediction[index])
           if self.highest_probability==None or probability>self.highest_probability:
              self.total_amount=amount
              self.highest_probability=probability                                 
                       
    def getData(self):
        if len(self.address)>0:
          self.src=self.address[0]
        if len(self.address)>1:
          self.dest=self.address[1]
        return {'date': self.date, 'dist': self.distance,'src':self.src,'dest':self.dest, 'amount':self.total_amount}