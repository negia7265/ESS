# request from client side is received as global server object
from flask import Flask, request, jsonify, render_template
# flask extension for handling cross origin resource sharing(CORS), making cross origin possible.
from flask_cors import CORS
from invoiceAI import InvoiceParser
import pandas as pd
from io import BytesIO

app = Flask(__name__, template_folder='template')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type' # configuring cors headers to content type

@app.route('/')
def index():
    return render_template('404.html'), 404

# api -  http://127.0.0.1:5000/parse_invoice/api/pdf
@app.route('/parse_invoice/api/pdf', methods=['POST'])
def extract_invoice_pdf():
    FILE = request.files['file']
    if not FILE:
        response=jsonify({'error': 'File Not Uploaded'})
    elif FILE.mimetype!='application/pdf':
        response= jsonify({'error': 'Invalid file type.'})
    else:        
        parser = InvoiceParser(BytesIO(FILE.read()),'pdf')
        response = jsonify(parser.getData())
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    return  response  #return json data to client side

@app.route('/parse_invoice/api/tsv', methods=['POST'])
def extract_invoice_image():
    data = request.get_json()
    if 'tsv' not in data or 'text' not in data or len(data)!=2 :
        response=jsonify({'error': 'Invalid data to process!'})
    else:    
        parser = InvoiceParser(data,'tsv')        
        response = jsonify(parser.getData())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return  response  #return json data to client side
  
if __name__=='__main__':
    app.run(debug=True) # Please do not set debug=True in production
