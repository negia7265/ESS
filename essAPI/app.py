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
from geopy.geocoders import GoogleV3
from geopy.distance import geodesic
app = Flask(__name__, template_folder='template')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# configuring cors headers to content type
app.config['CORS_HEADERS'] = 'Content-Type'

# Function to return the latest pdf attachment from the email inbox in bytes format

api_key = 'AIzaSyALB6uQiBGnyZAJMiS1MAT8ViJmRQea8W0'
geolocator = GoogleV3(api_key=api_key)


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
        response = jsonify({'error': 'Invalid file type.'})
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


@app.route('/get_threshold_distances', methods=['POST'])
def get_threshold_distances():
    data = request.json
    source_name = data.get('source_name', '')
    destination_name = data.get('destination_name', '')
    office_name = data.get('office_name', '')
    threshold = data.get('threshold', '')
    # source_name = "2722+5RC, Kasturba Nagar 3rd Cross St, Venkata Rathnam Nagar Extension,Venkata Rathinam Nagar, Adyar, Chennai"
    # destination_name = "24, Gangadhar Chetty Rd, Rukmani Colony, Sivanchetti Gardens, Bengaluru, Karnataka 560042"
    # office_name = "AMR Tech Park II, No. 23 & 24, Hongasandra, Hosur Main Road, Bengaluru, Karnataka 560068"

    # Perform geocoding for both locations
    location1 = geolocator.geocode(source_name)
    location2 = geolocator.geocode(destination_name)
    location3 = geolocator.geocode(office_name)
    # will return these too
    direction = ""
    status = ""

    if location1 and location2 and location3:
        source_to_destination = geodesic(
            (location1.latitude, location1.longitude), (location2.latitude, location2.longitude)).meters
        source_to_office = geodesic((location1.latitude, location1.longitude),
                                    (location3.latitude, location3.longitude)).meters
        destination_to_office = geodesic(
            (location2.latitude, location2.longitude), (location3.latitude, location3.longitude)).meters

        if (int(destination_to_office) <= int(source_to_office)):
            direction = "home_to_office"
            if (int(destination_to_office) <= threshold):
                status = "ESS_Granted"
            else:
                status = "ESS_Denied"
        elif (int(source_to_office) < int(destination_to_office)):
            direction = "office_to_home"
            if (int(source_to_office) <= threshold):
                status = "ESS_Granted"
            else:
                status = "ESS_Denied"

        return jsonify({
            "source_to_destination": int(source_to_destination),
            "source_to_office": int(source_to_office),
            "destination_to_office": int(destination_to_office),
            "direction": direction,
            "status": status
        })
    else:
        return jsonify({"error": "Geocoding failed for one or both locations"}), 400


if __name__ == '__main__':
    app.run(debug=True)  # Please do not set debug=True in production
