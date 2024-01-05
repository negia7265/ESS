from dateparser.search import search_dates 
from dateparser_data.settings import default_parsers
from nltk.tokenize import word_tokenize
import cv2
import os
import pytesseract
import numpy as np
import json
import re
import spacy
nlp = spacy.load("en_core_web_md")
parsers = [parser for parser in default_parsers if parser != 'relative-time']

def extract_distance(text):
    text=text.translate(str.maketrans('','','''()'''))
    #remove new line characters
    text=text.replace('\n', ' ')
    # lower case each letter of the word
    text=text.lower()
    distance=0
    # To ensure the match always starts with a number, use the \b word boundary anchor
    dist=re.findall(r'\b(\d+\.?\d*)[\s]*(km|kilomet|mile|meter|metre|foot|ft|yard|yd)',text)
    for i in dist:
        distance=max(distance,float(i[0]))                     
    return distance


# Out of all present packages dateparser is found to be the best as it's generalized
# One of the packages earlier used was datefinder
# datefinder could mistake like if two times date is written  
# example: "18 march 2001 18 march 2001" it is not able to parse date.
def extract_date(text):
    dates = search_dates(text,settings={'STRICT_PARSING': True,'PARSERS': parsers,'DATE_ORDER': 'DMY'})
    date=set()
    if dates==None:
        return date
    for d in dates:  #d[0] is the actual string format
        if d[1].year<2000: # by default if year is less than 2000 then continue with other dates.
            continue 
        date.add(d[1].strftime("%d-%m-%Y"))
    return date

def preprocess_img(img,img_decode):
    if img_decode:
        #Decode and convert to grayscale
        img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_GRAYSCALE)
         # Denoising Image
        img = cv2.fastNlMeansDenoising( img, None, 15, 7, 21 )   
    #Image Binarization
    img=cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # Perform morphological operations (erosion and dilation)
    kernel = np.ones((1, 1), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel)

def check_address(text):
    # Assumption: Address contains commas as seperator
    if ',' not in text: # Check if text doesn't have comma delimeter.
        return False
    # Assumption: Address Doesn't contain emails and hence no @ symbol 
    if '@' in text: # spacy considers text containing gmail address as location , so text containing gmail can never be address
        return False
    # this was an edge case found in invoices, through spacy NER , text containing thanks was also considered as location.
    if 'thank' in text : 
        return False
    doc = nlp(text)
    # Check if location is found in address 
    for entity in doc.ents:
        if entity.label_=='GPE' or entity.label_=='LOC':
            return True
    return False

relative_path = "essAPI"
# Get the absolute path of the tessdata directory
absolute_path = os.path.abspath(relative_path)
# absolute_path=os.getcwd() # for linux
def preprocess_address(text):
   #remove time from text
   position = re.search(r'\d{1,2}:\d{1,2}\s*(am|pm)?', text)
   if position is not None:
      text=text[position.end():]
   #remove unwanted characters from address
   text= re.sub(r"[^a-zA-Z0-9,\s/-]", "", text)
   return text

    
def get_address(img):
    address=[]
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (16,16))   
    dilation = cv2.dilate(img, rect_kernel, iterations = 3) 
    contours, _ = cv2.findContours(dilation,  cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    for cnt in contours[::-1]: 
        x, y, w, h = cv2.boundingRect(cnt)
        cropped = img[y:y + h, x:x + w]
        text=pytesseract.image_to_string(cropped,lang='eng',config=f'--tessdata-dir "{absolute_path}"').lower()
        if check_address(text):
            address.append(preprocess_address(text))
        if len(address)==2:
            return address
    return address   