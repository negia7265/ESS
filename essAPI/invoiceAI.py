import genie
import tensorflow as tf
import pandas as pd
import pdfplumber
from io import BytesIO
from generator import Generate_Extraction_Candidates
from model import Model
import os
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

gen=Generate_Extraction_Candidates()   

def init_amount_model():
    VOCAB_SIZE=2300
    EMBEDDING_SIZE=100
    NEIGHBOURS=10
    HEADS=4
    model = Model(VOCAB_SIZE, EMBEDDING_SIZE, NEIGHBOURS, HEADS)
    model.compile(
        loss=tf.keras.losses.BinaryCrossentropy(),
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        metrics=[
            'accuracy',
            tf.keras.metrics.Precision(),
            tf.keras.metrics.Recall(),
            tf.keras.metrics.AUC(),
        ],
    )
    init=pd.read_json('model_init.json')
    y_train=tf.constant(list(init['correct_candidate']))
    cand_pos=tf.constant(list(init['candidate_position']))
    neighbours=tf.constant(list(init['neighbour_id']))
    neighbour_positions=tf.constant(list(init['neighbour_relative_position']))
    field_id=tf.constant(list(init['field_id']))
    masks=tf.constant(list(init['mask']))
    model.train_on_batch((field_id,cand_pos,neighbours,neighbour_positions,masks),y_train) 
    model.load_weights('amount_2/model')
    return model

model=init_amount_model()

class InvoiceParser:
    def __init__(self,invoice_data,invoice_data_type):
        self.date=set()
        self.distance=set()
        self.amount=set()
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
        self.date=self.date.union(genie.extract_date(text))
        self.distance=self.distance.union(genie.extract_distance(text))
        
    def extract_amount(self,data,height,width):
        data.dropna(inplace=True)
        df=gen.get_extraction_candidates(data,10,None,height,width)
        df.reset_index(inplace=True)
        cand_pos=tf.constant(list(df['candidate_position']))
        neighbours=tf.constant(list(df['neighbour_id']))
        neighbour_positions=tf.constant(list(df['neighbour_relative_position']))
        field_id=tf.constant(list(df['field_id']))
        masks=tf.constant(list(df['mask']))
        if len(df['mask'])==0:
            return None
        prediction=model.predict((field_id,cand_pos,neighbours,neighbour_positions,masks))
        length=len(prediction)
        for index in range(length): 
            if prediction[index]>=0.5:
                self.amount.add(float(df.at[index,'text']))
       
    def getData(self):
        return {'date': list(self.date), 'distance': list(self.distance),'address': [], 'amount':list(self.amount)}
