import pytesseract
import re
import shutil
import os
import random
from IPython.display import display
try:
    from PIL import Image
except ImportError:
    import Image
import cv2
import numpy as np
from IPython.display import display, Image as IPImage
import pdfplumber
# load flask
from flask import Flask, jsonify, request
from flask import Flask
from flask_cors import CORS, cross_origin

# to be added
import datefinder
import nltk
import tensorflow as tf
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


app = Flask(__name__)
# nltk.download('omw-1.4')
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
stop_words.remove('m')  # meter word must not be removed during preprocessing
char_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,." "₹'

model = tf.keras.models.load_model('amount_2')


@app.route('/get_date', methods=['POST'])
def get_address():
    # Load Model
    # tagger = Classifier.load('ner-large')
    # Load PDF or Image

    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400
    extractedInformation = ""
    if file and file.filename.endswith('.pdf'):
        num_pages_to_extract = 2
        text = ''
        with pdfplumber.open(file) as pdf:
            for page_num in range(min(num_pages_to_extract, len(pdf.pages))):
                page = pdf.pages[page_num]
                page = page.dedupe_chars(tolerance=1)
                page_text = page.extract_text()
                text += page_text + '\n'
                extractedInformation = text
    elif file.filename.endswith(('.jpg', '.jpeg', '.png', '.PNG')):
        print("Image received")
        image_data = file.read()
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        img_pillow = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        extractedInformation = pytesseract.image_to_string(img_pillow)
    else:
        print('Invalid file format. Please upload a PDF file.')

    # add below functions

    def preprocess_text(text):
        # remove punctuation mark from the text
        text = text.translate(str.maketrans(
            '', '', ''',!"#%&'()*+-/:;<=>?@[\]^_`{|}~'''))
        # remove new line characters
        text = text.replace('\n', ' ')
        # lower case each letter of the word
        text = text.lower()
        # including space in beween {num}{word}
        text = re.sub(r'(\d+)([a-z]+)', r'\1 \2', text)
        # split the words into tokens
        tokens = word_tokenize(text)
        # remove stop words
        tokens = [word for word in tokens if word not in stop_words]
        # all words to root words
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(word) for word in tokens]
        # lemmatization
        lemmatized = [lemmatizer.lemmatize(token) for token in tokens]
        return lemmatized

    def extract_date(text):
        dates = list(datefinder.find_dates(text, strict=True))
        formatted_dates = [d.strftime("%d-%m-%Y") for d in dates]
        return formatted_dates

    def extract_distance(text):
        token = preprocess_text(text)
        distances = []
        km_keywords = {'km', 'kilomet', 'kilometr'}
        pattern = re.compile('[0-9]*.?[0-9]+$')

        for i in range(len(token) - 1):
            if pattern.match(token[i]) and token[i + 1] in km_keywords:
                distances.append(float(token[i]))

        return distances
    date = extract_date(extractedInformation)
    distance = extract_distance(extractedInformation)
    unique_date = list(set(date))
    unique_distance = list(set(distance))
    # real_distance = str(distance[0])+" KM"
    return {'status': "File Uploaded", 'date': unique_date, 'distance': unique_distance}


app.run()
