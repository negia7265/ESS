import genie
import tensorflow as tf
import pandas as pd
import pdfplumber
from io import BytesIO
from generator import Generate_Extraction_Candidates

gen=Generate_Extraction_Candidates()   

class InvoiceParser:
    def __init__(self,invoice_data):
        self.date=set()
        self.distance=set()
        self.amount=[]
        length=len(invoice_data['pdf'])      
        for i in range(length):  
            invoice = pdfplumber.open(BytesIO(invoice_data['pdf'][i]))
            for page in invoice.pages:
                page=page.dedupe_chars(tolerance=1)
                df=pd.DataFrame(page.extract_words())
                df['bottom']=df['bottom']-df['top']
                df['x1']=df['x1']-df['x0']
                df.rename(columns = {'bottom':'height','x1':'width'}, inplace = True)
                self.extract_amount(df,page.height,page.width)
                self.extract(page.extract_text())
            invoice.close()     
        length=len(invoice_data['page']) 
        for i in range(length):
            df=pd.DataFrame(invoice_data['page'][i]['tsv'],sep='\t')
            self.extract(df,invoice_data['page'][i]['text'])
            self.extract_amount(df,df.iloc[0]['height'],df.iloc[0]['width'])

           
    def extract(self,text):
        self.date=self.date.union(genie.extract_date(text))
        self.distance=self.distance.union(genie.extract_distance(text))
        
    def extract_amount(self,data,height,width):
        df=gen.get_extraction_candidates(data,10,true_candidates,height,width)
        cand_pos=tf.convert_to_tensor(list(df['candidate_position']))
        neighbours=tf.convert_to_tensor(list(df['neighbour_id']))
        neighbour_positions=tf.convert_to_tensor(list(df['neighbour_relative_position']))
        field_id=tf.convert_to_tensor(list(df['field_id']))
        masks=tf.convert_to_tensor(list(df['mask']))
        df=df.reset_index()
        model=tf.keras.models.load_model('amount_1.keras')
        prediction=model.predict((field_id,cand_pos,neighbours,neighbour_positions,masks))
        length=len(prediction)
        for index in range(length): 
            if prediction[index]>=0.5:
                self.amount.append(df.at[index,'text'])
       
    def getData(self):
        return {'date': list(self.date), 'distance': list(self.distance),'address': [], 'amount':self.amount}
