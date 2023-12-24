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

@app.route('/parse_invoice/api', methods=['POST'])
def extract_invoice_pdf():
    if len(request.files)!=1:
        response=jsonify({'error': 'Invalid number of invoice ! please upload 1 invoice image/pdf to process.'})
        response.status_code=404
        response.headers.add('Access-Control-Allow-Origin', '*')
        return  response  
    FILE = request.files['file']
    if FILE.mimetype=='application/pdf':        
        parser = InvoiceParser(BytesIO(FILE.read()),'pdf')
        response = jsonify(parser.getData())
    elif FILE.mimetype.startswith('image'):
        parser = InvoiceParser(FILE.read(),'image')        
        response = jsonify(parser.getData())         
    else:
        response=jsonify({'error': 'Invalid file type.'})
        response.status_code=404
    response.headers.add('Access-Control-Allow-Origin', '*')
    return  response  #return json data to client side
  
if __name__=='__main__':
    app.run(debug=True) # Please do not set debug=True in production
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

@app.route('/parse_invoice/api', methods=['POST'])
def extract_invoice_pdf():
    if len(request.files)!=1:
        response=jsonify({'error': 'Invalid number of invoice ! please upload 1 invoice image/pdf to process.'})
        response.status_code=404
        response.headers.add('Access-Control-Allow-Origin', '*')
        return  response  
    FILE = request.files['file']
    if FILE.mimetype=='application/pdf':        
        parser = InvoiceParser(BytesIO(FILE.read()),'pdf')
        response = jsonify(parser.getData())
    elif FILE.mimetype.startswith('image'):
        parser = InvoiceParser(FILE.read(),'image')        
        response = jsonify(parser.getData())         
    else:
        response=jsonify({'error': 'Invalid file type.'})
        response.status_code=404
    response.headers.add('Access-Control-Allow-Origin', '*')
    return  response  #return json data to client side
  
if __name__=='__main__':
    app.run(debug=True) # Please do not set debug=True in production
