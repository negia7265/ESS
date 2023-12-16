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
from flair.data import Sentence
from flair.nn import Classifier
from flair.models import SequenceTagger
# load flask

from flask import Flask, jsonify, request
from flask import Flask
from flask_cors import CORS, cross_origin
from city import cities

# For Date and Total
import datefinder
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

# Imports for Cost
import pandas as pd
import tensorflow as tf
from generator import Generate_Extraction_Candidates
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# configuring cors headers to content type
app.config['CORS_HEADERS'] = 'Content-Type'
gen = Generate_Extraction_Candidates()
model = tf.keras.models.load_model('amount_model.h5')

# tagger = Classifier.load('ner-large')
tagger = SequenceTagger.load('ner-large-model')
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
stop_words.remove('m')  # meter word must not be removed during preprocessing
char_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,." "₹'


@app.route('/get_data', methods=['POST'])
def get_data():

    amount = []

    def extract_amount(data, height, width):
        data.dropna(inplace=True)
        df = gen.get_extraction_candidates(data, 10, None, height, width)
        df.reset_index(inplace=True)
        cand_pos = tf.constant(list(df['candidate_position']))
        neighbours = tf.constant(list(df['neighbour_id']))
        neighbour_positions = tf.constant(
            list(df['neighbour_relative_position']))
        field_id = tf.constant(list(df['field_id']))
        masks = tf.constant(list(df['mask']))
        if len(df['mask']) == 0:
            return None
        prediction = model.predict(
            (field_id, cand_pos, neighbours, neighbour_positions, masks))
        length = len(prediction)
        for index in range(length):
            if prediction[index] >= 0.5:
                amount.append(float(df.at[index, 'text']))

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

                # add this
                df = pd.DataFrame(page.extract_words())
                df['bottom'] = df['bottom']-df['top']
                df['x1'] = df['x1']-df['x0']
                df.rename(columns={'bottom': 'height',
                          'x1': 'width', 'x0': 'left'}, inplace=True)
                extract_amount(df, page.height, page.width)

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

    # Date and Distance Fetching

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

    # Address Fetching

    sentence = Sentence(extractedInformation)

    # run NER over sentence
    tagger.predict(sentence)

    # print the sentence with all annotations
    # print(sentence)

    # Extract tokens labeled as 'LOC' from the named entities
    loc_tokens = [str(entity) for entity in sentence.get_spans(
        'ner') if 'LOC' in str(entity.labels[0])]

    # Print the list of 'LOC' tokens
    loc_texts_inside_quotes = [
        re.search(r'"([^"]*)"', loc_token).group(1) for loc_token in loc_tokens]

    # # Print the list of texts inside double quotes
    # print(loc_texts_inside_quotes)

    # cities = ["Kolkata", "Bengaluru", "Dehradun",
    #           "Chennai", "Mumbai", "Alwar", "Jaipur", "Pune"]
    states = ["Rajasthan", "Karnataka", "Uttarakhand"]

    def IndiaExist(temp):
        for i in range(len(temp)):
            if (temp[i] == "India"):
                return True

    def CityExist(city):
        for i in range(len(cities)):
            if (cities[i] == city):
                return True

    def StateExist(state):
        for i in range(len(states)):
            if (states[i] == state):
                return True

    list_again = []
    if (IndiaExist(loc_texts_inside_quotes)):
        for i in range(len(loc_texts_inside_quotes)):
            if (loc_texts_inside_quotes[i] == "India"):
                list_again.append(i)
    else:
        for i in range(len(loc_texts_inside_quotes)):
            if (CityExist(loc_texts_inside_quotes[i])):
                list_again.append(i)

    if len(list_again) >= 1:
        # Extract the substring from the beginning to the first occurrence of "India"
        substring_before_first_india = loc_texts_inside_quotes[:list_again[0] + 1]

        # Extract the substring from the first occurrence of "India" to the second occurrence of "India"
        if len(list_again) >= 2:
            substring_between_indias = loc_texts_inside_quotes[list_again[0] + 1:list_again[1]+1]
        else:
            substring_between_indias = loc_texts_inside_quotes[list_again[0] + 1:]

        # substring_between_indias = corrected_addresses[list_again[0] + 1:list_again[1] + 1]
    # removing white spaces

    cleaned_first_address = [word.strip()
                             for word in substring_before_first_india if word.strip()]
    cleaned_second_address = [word.strip()
                              for word in substring_between_indias if word.strip()]

    first_address = ', '.join(cleaned_first_address)
    second_address = ', '.join(cleaned_second_address)

    # Print the combined string
    return {'status': "File Uploaded", 'source': first_address, 'destination': second_address, 'date': unique_date, 'distance': unique_distance, 'cost': amount}


app.run()
