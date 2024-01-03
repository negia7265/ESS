# generate extraction candidates which could be the true entity to be extracted from invoice
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
import math
import json
import re
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
script_dir = os.path.dirname(os.path.abspath(__file__))
location_path = os.path.join(script_dir, 'vocab.json')
vocab = json.load(open(location_path, 'r'))


# detect type of candidate , if number then it could be amount / distance
# For now amount is taken into consideration and value 1 is returned for it
def detect_candidate(text):
    if pd.isna(text):
        return None
    if re.fullmatch(r"[0-9]*\.?[0-9]+", text):
        return 1  # amount type = 1
    return None


def preprocess(text):
    if pd.isna(text):
        return None
    text = str(text)
    # remove punctuation mark from the text
    text = text.translate(str.maketrans(
        '', '', ''',!"#%&'()*+-/:;<=>?@[\]^_`{|}~₹$'''))
    # lower case each letter of the word
    text = text.lower()
    if text in stop_words:
        return None
    # lemmatization , convert word to it's root word
    return lemmatizer.lemmatize(text)


class Generate_Extraction_Candidates:
    def __init__(self):
        self.width = None  # width of invoice page
        self.height = None  # height of invoice page
        # Example: The amount which is the total amount in the invoice page
        self.true_candidates = None
    # check if amount is the total amount of invoice or not with the help of json labels.

    def check_correctness(self, text):
        if pd.isna(text) or text == '':
            return None
        if re.fullmatch(r"[0-9]*\.?[0-9]+", text):
            if float(text) in self.true_candidates:
                return True
        return False

    # Form candidates dataframe which contains features of it's position and neighbour words.
    def get_candidates(self, df):
        cand = pd.DataFrame(columns=['field_id', 'candidate_position', 'neighbour_id',
                            'neighbour_relative_position', 'correct_candidate', 'left', 'top', 'width', 'height', 'text'])
        cand['left'] = df['left']
        cand['top'] = df['top']
        cand['width'] = df['width']
        cand['height'] = df['height']
        cand['field_id'] = df['text'].apply(detect_candidate)
        cand['text'] = df['text']
        if self.true_candidates != None:
            cand['correct_candidate'] = df['text'].apply(
                self.check_correctness)
        cand.dropna(subset=['field_id', 'top', 'width',
                    'height', 'left', 'text'], inplace=True)
        return cand

    # convert words to their numerical representation
    # During model training features are learned and made from these numbers through keras dense layers in machine learning
    def words_to_id(self, text):
        if pd.isna(text):
            return None
        if re.fullmatch(r"[0-9]*\.?[0-9]+", text):
            return vocab["number"]
        if text in vocab:
            return vocab[text]
        # rare means the words that does not exist in vocabulary
        return vocab["rare"]

    def get_extraction_candidates(self, df, num_neighbours, true_candidates, height, width):
        self.height = height
        self.width = width
        self.true_candidates = true_candidates
        df['text'] = df['text'].apply(preprocess)  # preprocess all the words
        candidates_df = self.get_candidates(df)
        df['text'] = df['text'].apply(self.words_to_id)
        df.dropna(subset=['text'], inplace=True)

        # Example: for each number get it's closest neighbour words with their positional features for model training
        for i, cand_row in candidates_df.iterrows():
            neighbour = dict()
            x1 = (cand_row['left']+cand_row['width']/2)/self.width
            y1 = (cand_row['top']+cand_row['height']/2)/self.height
            for j, neigh_row in df.iterrows():
                if i == j:
                    continue
                # earlier each word was converted to it's numerical value , so used here
                id = neigh_row['text']
                # positions of words need to be normalized
                # there centroid coordinate is taken in consideration
                x2 = (neigh_row['left']+neigh_row['width']/2)/self.width
                y2 = (neigh_row['top']+neigh_row['height']/2)/self.height
                # Ex. neighbours are searched towards left and half page upwards to the amount
                if x2 > x1 or y2 > y1+.02 or y2 < y1-0.1:
                    continue
                distance = math.dist([x1, y1], [x2, y2])
                if id in neighbour:
                    if distance < neighbour[id]['dist']:
                        neighbour[id] = {
                            'dist': distance,
                            'left': x2, 'top': y2
                        }
                else:
                    neighbour[id] = {
                        'dist': distance,
                        'left': x2, 'top': y2
                    }
            # if an entity has no neighbours, then there is no point to train it so continue .
            if len(neighbour) == 0:
                continue
            # sort to form n closest neighbours
            neighbour = dict(sorted(neighbour.items(), key=lambda item: item[1]['dist'])[
                             :num_neighbours])
            neighbours_remaining = num_neighbours-len(neighbour)
            neighbour_positions = list()
            neighbour_id = list()
            num_valid_values = 0
            for key in neighbour:
                # in vocab.json 18 and 19 are invalid values , they suggest no importance as amount neighbours
                # Model must not learn these values for true candidates. Example 1700 is amount but if it has no neighbours
                # it must not learn it.
                if key != 18 and key != 19:
                    num_valid_values += 1
                neighbour_id.append(key)
                neighbour_positions.append(
                    [neighbour[key]['left']-x1, neighbour[key]['top']-x2])

            # if a number is true amount and it does not has valid neighbours then do not take it into consideration for training
            if candidates_df.at[i, 'correct_candidate'] == True and num_valid_values == 0:
                continue
            # To make the data consistent , like if 10 neighbours are needed and only 4 neighbours are present then other values
            # need to be padded with zero's to feed machine learning model.
            while neighbours_remaining:  # used for masking
                neighbour_id.append(0)
                neighbour_positions.append([-1, -1])
                neighbours_remaining -= 1

            candidates_df.at[i, 'neighbour_id'] = neighbour_id
            candidates_df.at[i,
                             'neighbour_relative_position'] = neighbour_positions
            candidates_df.at[i, 'candidate_position'] = list(
                [float(x1), float(y1)])

        # remove the invalid rows from the dataframe , the invalid rows has undefined values .
        candidates_df.dropna(subset=['field_id', 'candidate_position', 'neighbour_id',
                             'neighbour_relative_position', 'left', 'top', 'width', 'height'], inplace=True)
        return candidates_df

    def generate_dataset(self, dir, annotated_file, num_neighbours):
        candidates = None
        invoices = os.listdir(dir)
        annotated = json.load(open(annotated_file, 'r+'))
        for invoice_dir in invoices:
            inv_csv = os.listdir(f'{dir}/{invoice_dir}')
            file = invoice_dir+'.pdf'
            true_candidates = [annotated[file]['amount']]
            for inv in inv_csv:
                df = pd.read_csv(f'{dir}/{invoice_dir}/{inv}')
                df = self.get_extraction_candidates(
                    df, num_neighbours, true_candidates, df['height'].max(), df['width'].max())
                if type(candidates) != None:
                    if not df.empty:
                        candidates = pd.concat([candidates, df])
                else:
                    candidates = df
        return candidates.reset_index()
