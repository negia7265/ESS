from dateparser.search import search_dates 
from dateparser_data.settings import default_parsers
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re # For preprocessing
from nltk.stem import WordNetLemmatizer
import cv2
import numpy as np
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
stop_words.remove('m')  #meter word must not be removed during preprocessing
parsers = [parser for parser in default_parsers if parser != 'relative-time']

def preprocess_text(text,ignore_root_word=False):
    #remove punctuation mark from the text
    text=text.translate(str.maketrans('','',''',!"#%&'()*+-/:;<=>?@[\]^_`{|}~$₹'''))
    #remove new line characters
    text=text.replace('\n', ' ')
    # lower case each letter of the word
    text=text.lower()
    #including space in beween {num}{word} 
    text=re.sub(r'(\d+)([a-z]+)', r'\1 \2', text)
    # split the words into tokens
    tokens=word_tokenize(text)
    # remove stop words 
    tokens = [word for word in tokens if word not in stop_words]
    if ignore_root_word:
        return tokens
    #all words to root words
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    #lemmatization
    lemmatized = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized

# heuristic/logic based approach to distance extraction
# To extract distance first representational learning could be applied , 
# distance could be scored as having "distance" as label or distance unit in front or left or down of a number
# Next feature is maximum number would be the exact distance along with labels.
 
def extract_distance(text):
    # it is necessary to preprocess text because distance could be written in 
    # format like 10Km , 10 kilometer, 30 kilometers ,etc. To convert it into 
    # root words and seperating number from word is necessary to extract distance.
    token=preprocess_text(text,ignore_root_word=False)
    distance=set()
    dist_pattern=re.compile('^(km|kilomet|met|m)\w*') # found these three types of words for distance in invoice.
    pattern = re.compile('[0-9]*.?[0-9]+$') # pattern to check for a number
    for i in range(len(token)-1):
      if pattern.match(token[i]) and dist_pattern.match(token[i+1]):
          distance.add(float(token[i]))
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
def preprocess_address_candidate(text):
    delimeter_count=0 # here comma(,) is the delimeter in address
    for char in text:
        delimeter_count+=1
    if delimeter_count==0:
        return None
    tokens=preprocess_text(text,ignore_root_word=True)
    location_found=False
    for token in tokens:
        if token in location:
            location_found=True 
            break
    if location_found==False:
        return None 
    
     
def get_indian_address_candidates(img):
    img=preprocess_img(img)
    # Specify structure shape and kernel size.Kernel size increases or decreases the area of the rectangle to be detected. 
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))   
    # Appplying dilation on the threshold image 
    dilation = cv2.dilate(img, rect_kernel, iterations = 4) 
    # Finding contours 
    contours, _ = cv2.findContours(dilation,  cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    indian_addresses=[]
    for cnt in contours[::-1]: 
        x, y, w, h = cv2.boundingRect(cnt) 
        cropped = img[y:y + h, x:x + w]
        text=pytesseract.image_to_string(cropped)
        text=preprocess_address_candidate(text)
        if text:
          indian_addresses.append(text)
    return indian_addresses