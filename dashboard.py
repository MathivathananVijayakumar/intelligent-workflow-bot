import streamlit as st
import pandas as pd
from database import fetch_all_emails, fetch_emails_by_category

# Page setup
st.set_page_config(page_title="Intelligent Workflow Dashboard", page_icon="📊", layout="wide")

st.title("📊 Intelligent Workflow Email Dashboard")
st.markdown("---")

# Fetch data
all_emails = fetch_all_emails()

# If no data
if not all_emails:
    st.info("No emails processed yet.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(all_emails)

# Remove MongoDB "_id" column if exists
if "_id" in df.columns:
    df = df.drop(columns=["_id"])

# Sidebar Filters
st.sidebar.header("📂 Filters")

categories = df["classification"].unique().tolist()
selected_categories = st.sidebar.multiselect("Select Classification", categories, default=categories)

# Filter data
filtered_df = df[df["classification"].isin(selected_categories)]

# Display
st.subheader(f"Showing {len(filtered_df)} Emails")
st.dataframe(filtered_df, use_container_width=True)

# Charts
st.markdown("### 📈 Email Category Distribution")
category_counts = filtered_df["classification"].value_counts()

st.bar_chart(category_counts)

# Optionally: Show individual email content
if st.checkbox("Show Email Details"):
    selected_email_idx = st.selectbox("Select Email", filtered_df.index)
    st.write(filtered_df.loc[selected_email_idx])

st.markdown("---")
st.caption("🚀 Intelligent Workflow Automation by MathivathananVijayakumar")
