import genie
import tensorflow as tf
import pandas as pd
import pdfplumber
import json
from io import BytesIO
from generator import Generate_Extraction_Candidates
import os
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO
gen=Generate_Extraction_Candidates()   
model=tf.keras.models.load_model('amount_model.keras')

class InvoiceParser:
    def __init__(self,invoice_data,invoice_data_type):
        self.date=dict({})
        self.distance=dict({})
        self.amount=dict({})
        if invoice_data_type=='pdf':
            invoice = pdfplumber.open(invoice_data)
            for page in invoice.pages:
                page=page.dedupe_chars(tolerance=1)
                df=pd.DataFrame(page.extract_words())
                df['bottom']=df['bottom']-df['top']
                df['x1']=df['x1']-df['x0']
                self.extract(page.extract_text())
                df.rename(columns = {'bottom':'height','x1':'width','x0':'left'}, inplace = True)
                self.extract_amount(df,page.height,page.width)
            invoice.close()
        else:     
            df=pd.read_csv(StringIO(invoice_data['tsv']), sep='\\t', encoding='utf_16le', engine='python', skipfooter=2,names=['level','page_num','block_num','par_num','line_num','word_num','left','top','width','height','conf','text'])
            self.extract(invoice_data['text'])
            self.extract_amount(df,df['height'].max(),df['width'].max())

           
    def extract(self,text):
        for d in genie.extract_date(text):
            self.date[d]=1
        for dist in genie.extract_distance(text):
            self.distance[dist]=1
                    
    def extract_amount(self,data,height,width):
        data.dropna(inplace=True)
        df=gen.get_extraction_candidates(data,10,None,height,width)
        df.reset_index(inplace=True)
        cand_pos=tf.constant(list(df['candidate_position']))
        neighbours=tf.constant(list(df['neighbour_id']))
        neighbour_positions=tf.constant(list(df['neighbour_relative_position']))
        field_id=tf.constant(list(df['field_id']))
        if len(df['field_id'])==0:
            return None
        prediction=model.predict((field_id,cand_pos,neighbours,neighbour_positions))
        length=len(prediction)
        for index in range(length): 
            probability=float(prediction[index])
            if probability>=0.5:
                amt=float(df.at[index,'text'])
                if amt in self.amount:
                   self.amount[amt]=max(self.amount[amt],probability)
                else:
                   self.amount[amt]=probability
                       
    def getData(self):
        return {'date': self.date, 'distance': self.distance,'address':dict({'address':1}), 'amount':self.amount}
