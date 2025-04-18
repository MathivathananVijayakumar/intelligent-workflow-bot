import imaplib
import email
from email.header import decode_header
import os

import streamlit as st

# Function to connect and fetch emails
def fetch_emails():
    EMAIL_USER = st.secrets["EMAIL_USER"]
    EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]

    # Connect to the Gmail server
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    # Login to your account
    imap.login(EMAIL_USER, EMAIL_PASSWORD)

    # Select the mailbox you want to check (inbox)
    imap.select("inbox")

    # Search for unseen emails
    status, messages = imap.search(None, 'UNSEEN')

    email_list = []

    for num in messages[0].split():
        status, data = imap.fetch(num, "(RFC822)")
        for response_part in data:
            if isinstance(response_part, tuple):
                # Parse a bytes email into a message object
                msg = email.message_from_bytes(response_part[1])

                # Decode email sender
                from_ = msg.get("From")
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

                body = ""
                attachments = []

                # If the email message is multipart
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                body = ""
                        elif "attachment" in content_disposition:
                            filename = part.get_filename()
                            if filename:
                                filepath = os.path.join("./temp", filename)
                                if not os.path.isdir("./temp"):
                                    os.mkdir("./temp")
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                attachments.append(filepath)
                else:
                    body = msg.get_payload(decode=True).decode()

                email_list.append({
                    "from": from_,
                    "subject": subject,
                    "body": body,
                    "attachments": attachments
                })

    imap.logout()
    return email_list
