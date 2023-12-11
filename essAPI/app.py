# request from client side is received as global server object
from flask import Flask, request, jsonify, render_template
# flask extension for handling cross origin resource sharing(CORS), making cross origin possible.
from flask_cors import CORS
from invoiceAI import InvoiceParser
from io import BytesIO

app = Flask(__name__, template_folder='template')
# The cross origin policy is required to be configured such that client server
# can communicate. The origin * , means that all type of devices can access it for now 
# but later it must be changed such that only specific devices can access the api 
# once deployed.
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type' # configuring cors headers to content type

@app.route('/')
def index():
    return render_template('404.html'), 404

# The following api can be called to parse pdf
# api -  http://127.0.0.1:5000/parse_invoice/api/pdf
# once deployed the api will get renamed
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

# This api end point receives tsv data of invoice image . The invoice image is 
# parsed in node.js and tsv data along with the text is received here to further
# parse and extract data from the content.
@app.route('/parse_invoice/api/tsv', methods=['POST'])
def extract_invoice_image():
    data = request.get_json()
    #json validation
    if 'tsv' not in data or 'text' not in data or len(data)!=2 :
        response=jsonify({'error': 'Invalid data to process!'})
    else:    
        parser = InvoiceParser(data,'tsv')        
        response = jsonify(parser.getData())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return  response  #return json data to client side
  
if __name__=='__main__':
    app.run(debug=True) # Please do not set debug=True in production
