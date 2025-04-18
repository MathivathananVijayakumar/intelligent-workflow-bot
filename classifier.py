import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to classify an email using OpenAI
def classify_email(subject, body):
    prompt = f"""
    You are an intelligent classification system.
    Classify the following email into one of the following categories:
    - Resume
    - Invoice
    - Support Ticket
    - Sales Inquiry
    - Others

    Email Subject: {subject}
    Email Body: {body}

    Respond ONLY with the category name.
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    classification = response.choices[0].message.content.strip()
    return classification
