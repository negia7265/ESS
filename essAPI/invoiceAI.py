import genie
import tensorflow as tf
import pandas as pd
import pdfplumber
from io import BytesIO
from generator import Generate_Extraction_Candidates
import os
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

gen=Generate_Extraction_Candidates()   

class InvoiceParser:
    def __init__(self,invoice_data,invoice_data_type):
        self.date=set()
        self.distance=set()
        self.amount=[]
        if invoice_data_type=='pdf':
            invoice = pdfplumber.open(invoice_data)
            for page in invoice.pages:
                page=page.dedupe_chars(tolerance=1)
                df=pd.DataFrame(page.extract_words())
                df['bottom']=df['bottom']-df['top']
                df['x1']=df['x1']-df['x0']
                df.rename(columns = {'bottom':'height','x1':'width','x0':'left'}, inplace = True)
                # self.extract_amount(df,page.height,page.width)
                self.extract(page.extract_text())
            invoice.close()
        else:     
            df = pd.read_csv(StringIO(invoice_data['tsv']), sep='\t',names=['level','page_num','block_num','par_num','line_num','word_num','left','top','width','height','conf','text'])
            self.extract(invoice_data['text'])
            #TODO NOT WORKING FOR NOW (MODEL IS CRASHED) self.extract_amount(df,df.iloc[0]['height'],df.iloc[0]['width'])

           
    def extract(self,text):
        self.date=self.date.union(genie.extract_date(text))
        self.distance=self.distance.union(genie.extract_distance(text))
        
    def extract_amount(self,data,height,width):
        data.dropna(inplace=True)
        df=gen.get_extraction_candidates(data,10,None,height,width)
        cand_pos=tf.constant(list(df['candidate_position']))
        neighbours=tf.constant(list(df['neighbour_id']))
        neighbour_positions=tf.constant(list(df['neighbour_relative_position']))
        field_id=tf.constant(list(df['field_id']))
        masks=tf.constant(list(df['mask']))
        model=tf.keras.models.load_model(f'{os.getcwd()}/amount_1.keras')
        df=df.reset_index()
        prediction=model.predict((field_id,cand_pos,neighbours,neighbour_positions,masks))
        length=len(prediction)
        for index in range(length): 
            if prediction[index]>=0.5:
                self.amount.append(df.at[index,'text'])
       
    def getData(self):
        return {'date': list(self.date), 'distance': list(self.distance),'address': [], 'amount':self.amount}
