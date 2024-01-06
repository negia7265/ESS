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
    distance_regex=r'\b(\d+\.?\d*)[\s]*(km|kilomet|mile|meter|metre|foot|ft|yard|yd)'
    dist=re.findall(distance_regex,text)
    for i in dist:
        distance=max(distance,float(i[0]))                     
    distance_regex=r'\bdistance\s*(kms?|kilometers?|kilometres?|miles?|foot|yard|meters?|metres?)\s*(\d*\.?\d+)'
    dist=re.findall(distance_regex,text)
    for i in dist:
        distance=max(distance,float(i[1]))                     
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

def preprocess_img(image):
    image=image.convert('RGB')
    image.save('300_dpi.jpg', dpi=(300, 300))  # Set 300 DPI
    #Decode and convert to grayscale
    img=cv2.imread('300_dpi.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
     # Denoising Image
    img = cv2.fastNlMeansDenoising( img, None, 15, 7, 21 )
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

def preprocess_address(text):
   #remove time from text
   position = re.search(r'\d{1,2}:\d{1,2}\s*(am|pm)?', text)
   if position is not None:
      text=text[position.end():]
   #remove unwanted characters from address
   text= re.sub(r"[^a-zA-Z0-9,\s/-]", "", text)
   text= re.sub(r"[\n\x0c]", "", text)
   return text

    
def get_address(img,preprocessed_img):
    address=[]
    ret, thresh1 = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (16,12))   
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 2) 
    contours, _ = cv2.findContours(dilation,  cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    for cnt in contours[::-1]: 
        x, y, w, h = cv2.boundingRect(cnt)
        cropped = preprocessed_img[y:y + h, x:x + w]
        text=pytesseract.image_to_string(cropped,lang='eng').lower()
        if check_address(text):
            address.append(preprocess_address(text))
        if len(address)==2:
            return address
    return address 