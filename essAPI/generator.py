# generate extraction candidates which could be the true entity to be extracted from invoice
import pandas as pd
import os
import math
import json
import re
script_dir = os.path.dirname(os.path.abspath(__file__))
location_path = os.path.join(script_dir, 'amount_vocab.json')
vocab = json.load(open(location_path, 'r'))
# vocab = json.load(open('./amount_vocab.json', 'r'))

def detect_candidate(text):
  if pd.isna(text):
     return None
  if re.fullmatch(r"[0-9]*\.?[0-9]+",text): 
      return 1  # amount type = 1
  return None

def preprocess(text):
    if pd.isna(text) or text=='':
        return None
    text=str(text)
    #remove punctuation mark from the text
    text=text.translate(str.maketrans('','',''',!"#%&'()*+-/:;<=>?@[\]^_`{|}~₹$'''))
    # lower case each letter of the word
    text=text.lower()
    if re.fullmatch(r"rm\s*[0-9]*\.?[0-9]+",text):
        text=re.sub(r'[^\d\.]','',text)
    return text

# check if amount is the total amount of invoice or not.
def check_correctness(text,amount):
    if pd.isna(text):
        return None
    if re.fullmatch(r"[0-9]*\.?[0-9]+", text):
        if float(text) ==float(amount):
            return True
    return False

# Form candidates dataframe which contains features of it's position and neighbour words.
def get_candidates(df,correct_amount):
    cand=pd.DataFrame(columns=['field_id','candidate_position','neighbour_id','neighbour_relative_position','correct_candidate','left','top','width','height','text'])
    cand['left']=df['left']
    cand['top']=df['top']
    cand['width']=df['width']
    cand['height']=df['height']
    cand['field_id']=df['text'].apply(detect_candidate)
    cand['text']=df['text']
    cand['correct_candidate']=df['text'].apply(check_correctness,amount=correct_amount)
    cand.dropna(subset=['field_id','top','width','height','left','text'],inplace=True)
    return cand


# convert words to their numerical representation
# During model training features are learned and made from these numbers through keras dense layers in machine learning
def words_to_id(text):
    if pd.isna(text):
        return None
    if re.fullmatch(r"[0-9]*\.?[0-9]+", text):
        return vocab["number"]
    if text in vocab:
        return vocab[text] 
    return vocab["rare"]  #rare means the words that does not exist in vocabulary     

def generate_amount_candidates(df,num_neighbours,correct_amount,height,width):    
    df['text']=df['text'].apply(preprocess)   #preprocess all the words 
    candidates_df=get_candidates(df,correct_amount)
    df['text']=df['text'].apply(words_to_id)
    df.dropna(subset=['text'],inplace=True)
    
    #Example: for each number get it's closest neighbour words with their positional features for model training  
    for i,cand_row in candidates_df.iterrows():               
        neighbour=dict()
        x1=(cand_row['left']+cand_row['width']/2)/width
        y1=(cand_row['top']+cand_row['height']/2)/height
        for j,neigh_row in df.iterrows():
            id=neigh_row['text'] # earlier each word was converted to it's numerical value , so used here 
            # positions of words need to be normalized 
            # there centroid coordinate is taken in consideration
            if id==vocab["number"]:
                continue
            x2=(neigh_row['left']+neigh_row['width']/2)/width
            y2=(neigh_row['top']+neigh_row['height']/2)/height
            #Ex. neighbours are searched towards left and half page upwards to the amount
            if x2 > x1 or y2 > y1+0.02 or y2 < y1-0.1:
                continue
            distance=math.dist([x1,y1],[x2,y2])
            if id in neighbour:
                if distance<neighbour[id]['dist']:
                    neighbour[id]={
                        'dist':distance,
                        'left':x2,'top':y2
                    }
            else:
                neighbour[id]={
                    'dist':distance,
                    'left':x2,'top':y2
                }     
        # if an entity has no neighbours, then there is no point to train it so continue .
        if len(neighbour)==0:
            continue
        # sort to form n closest neighbours
        neighbour=dict(sorted(neighbour.items(), key=lambda item: item[1]['dist'])[:num_neighbours])
        neighbours_remaining=num_neighbours-len(neighbour)
        neighbour_positions=list()
        neighbour_id=list()
        num_valid_values=0
        for key in neighbour:
            if key!=vocab['rare']: 
                num_valid_values+=1 
            neighbour_id.append(key)
            neighbour_positions.append([neighbour[key]['left']-x1,neighbour[key]['top']-x2])
        
        # if a number is true amount and it does not has valid neighbours then do not take it into consideration for training
        if candidates_df.at[i,'correct_candidate']==True and num_valid_values==0:
            continue
        # To make the data consistent , like if 10 neighbours are needed and only 4 neighbours are present then other values
        # need to be padded with zero's to feed machine learning model.
        while neighbours_remaining: #used for masking
            neighbour_id.append(0)  
            neighbour_positions.append([-1,-1]) 
            neighbours_remaining-=1

        candidates_df.at[i,'neighbour_id']=neighbour_id
        candidates_df.at[i,'neighbour_relative_position']=neighbour_positions
        candidates_df.at[i,'candidate_position']=list([float(x1),float(y1)]) 
        
    # remove the invalid rows from the dataframe , the invalid rows has undefined values . 
    candidates_df.dropna(subset=['field_id','candidate_position','neighbour_id','neighbour_relative_position','left','top','width','height'],inplace=True)
    return candidates_df