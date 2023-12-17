import genie # a custom set of functions made to extract date , preprocessing text and distance
import tensorflow as tf #used for machine learning
import pandas as pd # Most important to build dataframes used as dataset or input to ml model
import pdfplumber # best reliable open source project to parse pdf 
from generator import Generate_Extraction_Candidates
import os
import pytesseract
gen=Generate_Extraction_Candidates()   
model=tf.keras.models.load_model('amount_best_model_87.h5')

# This class receives either an invoice pdf or image , then with the help of heuristics, 
# best python packages, machine learning for information extraction from unstructured 
# invoice is done to extract date, distance, amount and address.  
class InvoiceParser:
    def __init__(self,invoice_data,invoice_data_type):
        # dictionary is used to get unique instances of date, distance, amount
        self.date=dict({})
        self.distance=dict({})
        self.amount=dict({})
        if invoice_data_type=='pdf':
            invoice = pdfplumber.open(invoice_data)
            for page in invoice.pages:
                # dedupe chars is a method which removes overlapped lines in a page
                # bold fonts can be considered double /overlapped lines so it is used here.  
                page=page.dedupe_chars(tolerance=1)
                # The text positional features along with text itself is extracted from 
                # pdf as well as image as ml model input
                df=pd.DataFrame(page.extract_words())
                df['bottom']=df['bottom']-df['top']
                df['x1']=df['x1']-df['x0']
                self.extract(page.extract_text())
                df.rename(columns = {'bottom':'height','x1':'width','x0':'left'}, inplace = True)
                self.extract_amount(df,page.height,page.width)
            invoice.close()
        else:  
            img=genie.preprocess_img(invoice_data)  
            text=pytesseract.image_to_string(img,lang='eng',config=f'--tessdata-dir "{os.getcwd()}"')
            self.extract(text)
            # dataframe contains positional features of each word present in invoice.
            df=pytesseract.image_to_data(img,lang='eng',config=f'--tessdata-dir "{os.getcwd()}"', output_type='data.frame')
            # Tesseract ocr provides image dimensions in it's dataframe 
            self.extract_amount(df,df['height'].max(),df['width'].max())

  # The date , distance are accurate and has less candidates so there probability is set
  # to 100% such and returned to client side.
    def extract(self,text):
        print(text)
        for d in genie.extract_date(text):
            self.date[d]=1
        for dist in genie.extract_distance(text):
            self.distance[dist]=1
                    
    def extract_amount(self,data,height,width):
        #Height and width are dimensions of invoice
        data.dropna(inplace=True)
        # amounts are extracted such as tax, subtotal, due, total amount these are known candidates
        df=gen.get_extraction_candidates(data,10,None,height,width)
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
            probability=float(prediction[index])
            amt=float(df.at[index,'text'])
            if amt in self.amount:
                self.amount[amt]=max(self.amount[amt],probability)
            else:
                self.amount[amt]=probability
                       
    def getData(self):
        # select best 4 scoring amounts and return all the invoice details
        # 4 is a random number it depends upon need of the developer/client
        self.amount=dict(sorted(self.amount.items(), key=lambda item: item[1],reverse=True)[:4])
        return {'date': self.date, 'distance': self.distance,'address':dict({'address':1}), 'amount':self.amount}
