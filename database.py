from pymongo import MongoClient
import streamlit as st

# Connect to MongoDB
def get_database():
    MONGO_URI = st.secrets["MONGO_URI"]
    client = MongoClient(MONGO_URI)
    db = client["email_workflow_db"]  # You can change database name
    return db

# Save email data into MongoDB
def save_email_data(email_data):
    db = get_database()
    collection = db["emails"]
    collection.insert_one(email_data)

# Fetch all saved emails
def fetch_all_emails():
    db = get_database()
    collection = db["emails"]
    return list(collection.find())

# Fetch emails by classification
def fetch_emails_by_category(category):
    db = get_database()
    collection = db["emails"]
    return list(collection.find({"classification": category}))
