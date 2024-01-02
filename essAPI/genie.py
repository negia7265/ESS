from dateparser.search import search_dates 
from dateparser_data.settings import default_parsers
from nltk.tokenize import word_tokenize
import cv2
import os
import pytesseract
import numpy as np
import json
import re
script_dir = os.path.dirname(os.path.abspath(__file__))
location_path = os.path.join(script_dir, 'location.json')

parsers = [parser for parser in default_parsers if parser != 'relative-time']
location = json.load(open(location_path))

def extract_distance(text):
    text=text.translate(str.maketrans('','','''()'''))
    #remove new line characters
    text=text.replace('\n', ' ')
    # lower case each letter of the word
    text=text.lower()
    distance=0
    # To ensure the match always starts with a number, use the \b word boundary anchor
    dist=re.findall(r'\b(\d+\.?\d*)[\s]*(km|kilomet)',text)
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
        date.add(d[1].strftime("%d-%m-%Y"))
    return date

def preprocess_img(img):
    # Decode and convert to grayscale
    img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_GRAYSCALE)
    # Denoising Image
    img = cv2.fastNlMeansDenoising( img, None, 15, 7, 21 )   
    # Image Binarization
    img=cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # Perform morphological operations (erosion and dilation)
    kernel = np.ones((1, 1), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel)

# iterate each candidate and preprocess to remove words which are non relevant to address
def contains_indian_city_or_country_name(text):
    if ',' not in text:
        return False 
    text=text.translate(str.maketrans('','',''',!"#%&'()*+-/:;<=>?@[\]^_`{|}~$₹'''))
    #remove new line character
    text=text.replace('\n', ' ')
    # lower case each letter of the word
    text=text.lower()
    # split the words into tokens
    tokens=word_tokenize(text)
    for word in tokens:
       if word in location:
          return True
    return False

relative_path = "essAPI"
# Get the absolute path of the tessdata directory
absolute_path = os.path.abspath(relative_path)

    
def get_address(img):
    address=[]
    ret, thresh1 = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (16,16))   
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 3) 
    contours, _ = cv2.findContours(dilation,  cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    for cnt in contours[::-1]: 
        x, y, w, h = cv2.boundingRect(cnt)
        cropped = img[y:y + h, x:x + w]
        text=pytesseract.image_to_string(cropped,lang='eng',config=f'--tessdata-dir "{absolute_path}"')
        if contains_indian_city_or_country_name(text):
            address.append(text)
        if len(address)==2:
            return address
    return address   