import streamlit as st
from email_reader import fetch_emails
from document_parser import parse_attachments
from classifier import classify_email
from responder import generate_response
from database import save_to_db

st.title("📩 Intelligent Workflow Automation Bot")

if st.button("Process New Emails"):
    emails = fetch_emails()
    for email in emails:
        classification = classify_email(email['subject'], email['body'])
        extracted_data = parse_attachments(email['attachments'])
        response_text = generate_response(classification, extracted_data)
        save_to_db(email, classification, extracted_data, response_text)
        st.success(f"Processed email from {email['from']} - classified as {classification}")

st.info("System Ready 🚀")
