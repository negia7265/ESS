from flask import Flask, request, jsonify, render_template, send_file
# flask extension for handling cross origin resource sharing(CORS), making cross origin possible.
from flask_cors import CORS
from invoiceAI import InvoiceParser
from io import BytesIO
import imaplib
import email
from email.header import decode_header
import os
import io
app = Flask(__name__, template_folder='template')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# configuring cors headers to content type
app.config['CORS_HEADERS'] = 'Content-Type'

# Function to return the latest pdf attachment from the email inbox in bytes format


def fetch_latest_pdf_attachment(email_user, email_pass):

    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_user, email_pass)

    # Select the mailbox (inbox in this case)
    mail.select("inbox")

    # Search for emails with "OLA" or "Uber" in the subject
    status, messages = mail.search(
        None, '(OR SUBJECT "Rapido Invoice" SUBJECT "Invoice for your Ride")')

    # Fetch the most recent email
    latest_msg_id = messages[0].split()[-1]
    _, latest_msg_data = mail.fetch(latest_msg_id, "(RFC822)")
    latest_raw_email = latest_msg_data[0][1]
    latest_msg = email.message_from_bytes(latest_raw_email)
    pdf_attachment = None
    for part in latest_msg.walk():
        if part.get_content_type() == "application/pdf":
            print("PDF found")
            pdf_attachment = part.get_payload(decode=True)
            break
    # Process the PDF attachment
    if pdf_attachment:
        # Save the PDF content to a file with the appropriate extension
        pdf_filename = "latest_attachment.pdf"
        with open(pdf_filename, "wb") as pdf_file:
            pdf_file.write(pdf_attachment)

    # Close the connection
    mail.close()
    mail.logout()
    return pdf_attachment


@app.route('/')
def index():
    return render_template('404.html'), 404


@app.route('/parse_invoice/api', methods=['POST'])
def extract_invoice_pdf():
    if len(request.files) != 1:
        response = jsonify(
            {'error': 'Invalid number of invoice ! please upload 1 invoice image/pdf to process.'})
        # TODO check
        response.status_code = 404
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    FILE = request.files['file']
    if FILE.mimetype == 'application/pdf':
        parser = InvoiceParser(BytesIO(FILE.read()), 'pdf')
        response = jsonify(parser.getData())
    elif FILE.mimetype.startswith('image'):
        parser = InvoiceParser(FILE.read(), 'image')
        response = jsonify(parser.getData())
    else:
        # TODO check
        response = jsonify({'error': 'Invalid file type.'})
        response.status_code = 404
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response  # return json data to client side


@app.route('/get_latest_pdf', methods=['GET'])
def get_latest_pdf():
    email_user = 'blackpearl7579@gmail.com'
    email_pass = 'ddvh wnep mxmr ydso'

    # Fetch the latest PDF attachment
    pdf_attachment = fetch_latest_pdf_attachment(email_user, email_pass)

    # Check if PDF is found
    if pdf_attachment:
        # doing this conversion cause the original data was in bytes converting it into file form
        pdf_file_like = io.BytesIO(pdf_attachment)
        return send_file(
            pdf_file_like,
            download_name="latest_attachment.pdf",
            mimetype="application/pdf"
        )
    else:
        return "No PDF attachment found in the latest email."


if __name__ == '__main__':
    app.run(debug=True)  # Please do not set debug=True in production
