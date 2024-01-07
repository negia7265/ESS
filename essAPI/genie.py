from nltk.tokenize import word_tokenize
import cv2
import os
import pytesseract
import numpy as np
import json
import re
import spacy
nlp = spacy.load("en_core_web_md")


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