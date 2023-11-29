# request from client side is received as global server object
from flask import Flask, request, jsonify, render_template
# flask extension for handling cross origin resource sharing(CORS), making cross origin possible.
from flask_cors import CORS
from invoiceAI import InvoiceParser
import pandas as pd

app = Flask(__name__, template_folder='template')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type' # configuring cors headers to content type

@app.route('/')
def index():
    return render_template('404.html'), 404

#TODO check error in each part of api which could occur to wrong data submission
@app.route('/extractInvoice/', methods=['POST'])
def extractInvoice():
    data = request.get_json()
    parser = InvoiceParser(data)        
    response = jsonify(parser.getData())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return  response  #return json data to client side
  
if __name__=='__main__':
    app.run(debug=True) # Please do not set debug=True in production
