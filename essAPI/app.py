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
from datetime import datetime, timedelta
import zipfile
app = Flask(__name__, template_folder='template')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# configuring cors headers to content type
app.config['CORS_HEADERS'] = 'Content-Type'

# Function to return the latest pdf attachment from the email inbox in bytes format

api_key = 'AIzaSyALB6uQiBGnyZAJMiS1MAT8ViJmRQea8W0'
# api_key = 'AIzaSyCXrR0hZ22X-nlMkwWK2pwt81mEJhL9V3Y'
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


def fetch_invoice_data_last_num_days(email_user, email_pass, day):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_user, email_pass)

    # Select the mailbox (inbox in this case)
    mail.select("inbox")

    # Calculate the date 'day' days ago
    days_ago = (datetime.now() - timedelta(days=day)).strftime("%d-%b-%Y")

    # Search for emails with specific subjects received in the last 'day' days
    status, messages = mail.search(
        None, f'(OR SUBJECT "Rapido Invoice" SUBJECT "Invoice for your Ride") SINCE {days_ago}'
    )

    invoice_data = []

    for msg_id in messages[0].split():
        _, msg_data = mail.fetch(msg_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Extract subject, date, and time information
        subject = msg["Subject"]
        date_received = datetime.strptime(
            msg["Date"], "%a, %d %b %Y %H:%M:%S %z")
        sender_address = msg.get("From", "")
        # Store date and time as separate strings
        formatted_date = date_received.strftime("%d-%b-%Y")
        formatted_time = date_received.strftime("%I:%M %p %Z")

        # Append data to the invoice_data array
        invoice_data.append({
            "subject": subject,
            "date_received": formatted_date,
            "time_received": formatted_time,
            "sender_address": sender_address
        })

    mail.close()
    mail.logout()

    return invoice_data


def fetch_pdfs_last_num_days(email_user, email_pass, day):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_user, email_pass)

    # Select the mailbox (inbox in this case)
    mail.select("inbox")

    # Calculate the date 10 days ago
    ten_days_ago = (datetime.now() - timedelta(days=day)).strftime("%d-%b-%Y")

    # Search for emails with "OLA" or "Uber" in the subject received in the last 10 days
    status, messages = mail.search(
        None, f'(OR SUBJECT "Rapido Invoice" SUBJECT "Invoice for your Ride") SINCE {ten_days_ago}'
    )

    pdf_attachments = []
    for msg_id in messages[0].split():
        _, msg_data = mail.fetch(msg_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        for part in msg.walk():
            if part.get_content_type() == "application/pdf":
                print("PDF found")
                pdf_attachment = part.get_payload(decode=True)
                pdf_attachments.append(pdf_attachment)

    mail.close()
    mail.logout()

    return pdf_attachments


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


@app.route('/get_last_num_days_pdf', methods=['POST'])
def get_pdf_last_num_days():
    email_user = 'blackpearl7579@gmail.com'
    email_pass = 'ddvh wnep mxmr ydso'
    data = request.json
    days = data.get('days', '')
    day = int(days)

    pdf_attachments = fetch_pdfs_last_num_days(email_user, email_pass, day)

    # Check if any PDFs are found
    if pdf_attachments:
        # Create a zip file to store multiple PDFs
        zip_file = io.BytesIO()
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            for index, pdf_attachment in enumerate(pdf_attachments):
                pdf_filename = f"attachment_{index + 1}.pdf"
                zipf.writestr(pdf_filename, pdf_attachment)

        # Seek to the beginning of the zip file
        zip_file.seek(0)

        return send_file(
            zip_file,
            download_name="latest_attachments.zip",
            mimetype="application/zip"
        )
    else:
        return "No PDF attachments found in the last 10 days."


@app.route('/fetch_invoice_data_last_num_days', methods=['POST'])
def get_invoice_data_last_num_days():
    email_user = 'blackpearl7579@gmail.com'
    email_pass = 'ddvh wnep mxmr ydso'
    data = request.json
    days = data.get('days', '')
    day = int(days)

    invoice_data = fetch_invoice_data_last_num_days(
        email_user, email_pass, day)

    # Check if any PDFs are found
    if invoice_data:
        # Create a zip file to store multiple PDFs
        invoice_data.reverse()
        return jsonify({"invoice_data": invoice_data})
    else:
        return "No PDF data found in the last 10 days."


@app.route('/get_threshold_distances', methods=['POST'])
def get_threshold_distances():
    data = request.json
    source_name = data.get('source_name', '')
    destination_name = data.get('destination_name', '')
    office_name = data.get('office_name', '')
    threshold = data.get('threshold', '')
    homethreshold = data.get('homethreshold', '')
    homeAddress = data.get('homeAddress', '')
    print(source_name, destination_name, office_name,
          threshold, homethreshold, homeAddress)
    # source_name = "2722+5RC, Kasturba Nagar 3rd Cross St, Venkata Rathnam Nagar Extension,Venkata Rathinam Nagar, Adyar, Chennai"
    # destination_name = "24, Gangadhar Chetty Rd, Rukmani Colony, Sivanchetti Gardens, Bengaluru, Karnataka 560042"
    # office_name = "AMR Tech Park II, No. 23 & 24, Hongasandra, Hosur Main Road, Bengaluru, Karnataka 560068"

    # Perform geocoding for both locations

    location1 = geolocator.geocode(source_name)
    location2 = geolocator.geocode(destination_name)
    location3 = geolocator.geocode(office_name)
    location4 = geolocator.geocode(homeAddress)
    # will return these too
    direction = ""
    status = ""
    print(homeAddress)
    if location1 and location2 and location3:
        source_to_destination = geodesic(
            (location1.latitude, location1.longitude), (location2.latitude, location2.longitude)).meters
        source_to_office = geodesic((location1.latitude, location1.longitude),
                                    (location3.latitude, location3.longitude)).meters
        destination_to_office = geodesic(
            (location2.latitude, location2.longitude), (location3.latitude, location3.longitude)).meters
        home_to_source = geodesic((location4.latitude, location4.longitude),
                                  (location1.latitude, location1.longitude)).meters
        home_to_destination = geodesic(
            (location4.latitude, location4.longitude), (location2.latitude, location2.longitude)).meters
        print(source_to_destination)

        if (int(destination_to_office) <= int(source_to_office)):
            direction = "home_to_office"
            if (int(destination_to_office) <= threshold and int(home_to_source) <= homethreshold):
                status = "ESS_Granted"
            else:
                status = "ESS_Denied"
        elif (int(source_to_office) < int(destination_to_office)):
            direction = "office_to_home"
            if (int(source_to_office) <= threshold and int(home_to_destination) <= homethreshold):
                status = "ESS_Granted"
            else:
                status = "ESS_Denied"
        response = jsonify({
            "source_to_destination": int(source_to_destination),
            "source_to_office": int(source_to_office),
            "destination_to_office": int(destination_to_office),
            "direction": direction,
            "status": status
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        return jsonify({"error": "Geocoding failed for one or both locations"}), 400


if __name__ == '__main__':
    app.run(debug=True)  # Please do not set debug=True in production
