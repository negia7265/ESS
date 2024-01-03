import imaplib
import email
from email.header import decode_header
# from pdfminer.high_level import extract_text
import os

# Email account credentials
email_user = 'blackpearl7579@gmail.com'
email_pass = 'ddvh wnep mxmr ydso'

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(email_user, email_pass)

# Select the mailbox (inbox in this case)
mail.select("inbox")

# Search for emails with "OLA" or "Uber" in the subject
status, messages = mail.search(
    None, '(OR SUBJECT "Rapido Invoice" SUBJECT "Uber")')

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
