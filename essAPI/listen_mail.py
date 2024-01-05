from flask import Flask, send_file
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import zipfile

import os
import io
app = Flask(__name__)


def fetch_latest_pdf_attachment(email_user, email_pass):
    # Connect to the IMAP server
    # email_user = 'blackpearl7579@gmail.com'
    # email_pass = 'ddvh wnep mxmr ydso'

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
    print(type(latest_msg))
    # Check if the email has PDF attachments
    # latest_pdf_attachment = None
    # for part in latest_msg.iter_attachments():
    #     if part.get_content_type() == "application/pdf":
    #         latest_pdf_attachment = part.get_payload(decode=True)
    #         break
    pdf_attachment = None
    for part in latest_msg.walk():
        if part.get_content_type() == "application/pdf":
            print("PDF found")
            pdf_attachment = part.get_payload(decode=True)
            break
    print(type(pdf_attachment))
    # Process the PDF attachment
    if pdf_attachment:
        # Save the PDF content to a file with the appropriate extension
        pdf_filename = "latest_attachment.pdf"
        with open(pdf_filename, "wb") as pdf_file:
            pdf_file.write(pdf_attachment)
    # # Process the latest PDF attachment
    # if latest_pdf_attachment:
    #     # Extract text from PDF using pdfminer
    #     # pdf_text = extract_text(latest_pdf_attachment)

    #     # You can now process the extracted text as needed
    #     print(f"Extracted text from the latest PDF in email")
    # else:
    #     print("No PDF attachment found in the latest email.")

    # Close the connection
    mail.close()
    mail.logout()
    return pdf_attachment


def fetch_pdfs_last_10_days(email_user, email_pass):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_user, email_pass)

    # Select the mailbox (inbox in this case)
    mail.select("inbox")

    # Calculate the date 10 days ago
    ten_days_ago = (datetime.now() - timedelta(days=10)).strftime("%d-%b-%Y")

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


@app.route('/get_latest_pdf', methods=['GET'])
def get_latest_pdf():
    email_user = 'blackpearl7579@gmail.com'
    email_pass = 'ddvh wnep mxmr ydso'

    # Fetch the latest PDF attachment
    # pdf_attachment = fetch_latest_pdf_attachment(email_user, email_pass)

    # # Check if PDF is found

    # if pdf_attachment:
    #     # doing this conversion cause the original data was in bytes converting it into file form
    #     pdf_file_like = io.BytesIO(pdf_attachment)
    #     return send_file(
    #         pdf_file_like,
    #         download_name="latest_attachment.pdf",
    #         mimetype="application/pdf"
    #     )
    # else:
    #     return "No PDF attachment found in the latest email."

    pdf_attachments = fetch_pdfs_last_10_days(email_user, email_pass)

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


if __name__ == '__main__':
    app.run(debug=True)
