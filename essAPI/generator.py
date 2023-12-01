import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import os
import math
import json 
import re
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
vocab=json.load(open('vocab.json','r'))

def detect_candidate(text):
  if pd.isna(text):
     return None
  if re.fullmatch(r"[0-9]*\.?[0-9]+",text):
      return None
  #TODO work has to be done here to extract candidates
  return None

def preprocess(text):
    if pd.isna(text):
        return None
    text=str(text)
    #remove punctuation mark from the text
    text=text.translate(str.maketrans('','',''',!"#%&'()*+-/:;<=>?@[\]^_`{|}~₹$'''))
    # lower case each letter of the word
    text=text.lower()
    if text in stop_words:
        return None
    # convert text word to it's root word 
    stemmer = PorterStemmer()
    text = stemmer.stem(text) 
    #lemmatization
    return lemmatizer.lemmatize(text)

class Generate_Extraction_Candidates:
    def __init__(self):
        self.width=None
        self.height=None
        self.true_candidates=None
    def check_correctness(self,text):
        if pd.isna(text) or text=='':
            return None
        if re.fullmatch(r"[0-9]*\.?[0-9]+",text):
            if float(text) in self.true_candidates:
                return True
        return False
    def get_candidates(self,df):
        cand=pd.DataFrame(columns=['field_id','candidate_position','neighbour_id','neighbour_relative_position','mask','correct_candidate','left','top','width','height'])
        cand['left']=df['left']
        cand['top']=df['top']
        cand['width']=df['width']
        cand['height']=df['height']
        cand['field_id']=df['text'].apply(detect_candidate)
        if self.true_candidates!=None:
           cand['correct_candidate']=df['text'].apply(self.check_correctness)
        cand.dropna(subset=['field_id','top','width','height','left'],inplace=True)
        return cand
    def words_to_id(self,text):
        if not pd.isna(text) and text.isalpha():
            if text in vocab:
                return vocab[text]
        return None        

        
    def get_extraction_candidates(self,df,num_neighbours,true_candidates,height,width):
        self.height=height
        self.width=width
        self.true_candidates=true_candidates
        df['text']=df['text'].apply(preprocess)
        candidates_df=self.get_candidates(df)
        df['text']=df['text'].apply(self.words_to_id)
        df.dropna(subset=['text'],inplace=True)
        #Number of rows in dataframe
        # Extract neighbour id's, neighbour relative positions,  
        # mask to check which words are effective or not for data extraction.
        for i,cand_row in candidates_df.iterrows():               
            neighbour=dict()
            x1=(cand_row['left']+cand_row['width']/2)/self.width
            y1=(cand_row['top']+cand_row['height']/2)/self.height
            for j,neigh_row in df.iterrows():
                if i==j:
                    continue
                id=neigh_row['text']
                x2=(neigh_row['left']+neigh_row['width']/2)/self.width
                y2=(neigh_row['top']+neigh_row['height']/2)/self.height
                if x2>x1 or y2>y1+.2 or y2<y1-0.1:  #TODO put these values in parameters
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
                                        
            if len(neighbour)==0:
                continue
            neighbour=dict(sorted(neighbour.items(), key=lambda item: item[1]['dist'])[:num_neighbours])
            neighbours_remaining=num_neighbours-len(neighbour)
            mask=list()
            neighbour_positions=list()
            neighbour_id=list()
            for key in neighbour:
                neighbour_id.append(key)
                neighbour_positions.append([neighbour[key]['left']-x1,neighbour[key]['top']-x2])
                mask.append(False)
            while neighbours_remaining: 
                neighbour_id.append(0)
                neighbour_positions.append([-1,-1])
                mask.append(True)
                neighbours_remaining-=1

            candidates_df.at[i,'neighbour_id']=neighbour_id
            candidates_df.at[i,'neighbour_relative_position']=neighbour_positions
            candidates_df.at[i,'mask']=mask
            candidates_df.at[i,'candidate_position']=list([float(x1),float(y1)]) 
        #TODO some of the candidate positions are coming na ,  dont know reason behind it , checked everything but still candidate positions are invalid sometime.
        candidates_df.dropna(subset=['field_id','candidate_position','neighbour_id','neighbour_relative_position','mask','left','top','width','height'],inplace=True)
        return candidates_df

    def generate_dataset(self,dir,annotated_file,num_neighbours):
        candidates=None
        invoices=os.listdir(dir)
        annotated=json.load(open(annotated_file,'r+'))
        for invoice_dir in invoices:
            inv_csv=os.listdir(f'{dir}/{invoice_dir}')
            file=invoice_dir+'.pdf'
            true_candidates=[annotated[file]['amount']] 
            for inv in inv_csv:
               df=pd.read_csv(f'{dir}/{invoice_dir}/{inv}')
               df=self.get_extraction_candidates(df,num_neighbours,true_candidates,df.iloc[0]['height'],df.iloc[0]['width'])
               if type(candidates)!=None:
                 if not df.empty:
                    candidates=pd.concat([candidates,df])
               else:
                 candidates=df  
        return candidates.reset_index()
