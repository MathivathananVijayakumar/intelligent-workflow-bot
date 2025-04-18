import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to generate a response email
def generate_response(classification, extracted_data):
    attachment_summary = "\n".join([f"File: {item['file']} - Content Preview: {item['content'][:200]}..." for item in extracted_data])

    prompt = f"""
    You are a professional assistant. Based on the classification and attached document summaries below, generate a polite, appropriate response email.

    Classification: {classification}
    Document Summary:
    {attachment_summary}

    The response should be formal, short, and relevant.
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    generated_email = response.choices[0].message.content.strip()
    return generated_email
