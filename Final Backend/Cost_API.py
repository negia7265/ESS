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
import tensorflow as tf
import pandas as pd
import numpy as np
from IPython.display import display, Image as IPImage
import pdfplumber
# load flask
from flask import Flask, jsonify, request
from flask import Flask
from flask_cors import CORS, cross_origin


from generator import Generate_Extraction_Candidates
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
from keras.models import load_model

app = Flask(__name__)
gen = Generate_Extraction_Candidates()
# model = tf.keras.models.load_model('amount_model.h5')
model = load_model('amount_model.h5')


@app.route('/get_date', methods=['POST'])
def get_amount():

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

        # specifying nummber of pages to be read of the pdf.
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
        # df = pd.read_csv(StringIO(invoice_data['tsv']), sep='\\t', encoding='utf_16le', engine='python', skipfooter=2, names=[
        #                  'level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height', 'conf', 'text'])
        # extract_amount(df, df['height'].max(), df['width'].max())
    else:
        print('Invalid file format. Please upload a PDF file.')

    return {'status': "File Uploaded", 'amount': amount}


app.run()
