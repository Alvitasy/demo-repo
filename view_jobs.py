import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os

# --- Load Supabase credentials ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Streamlit page config ---
st.set_page_config(page_title="Athena.7t | Job Board", layout="wide")
st.title("💼 Job Openings at Athena.7t")

# --- Session state for selected job ---
if "selected_job_id" not in st.session_state:
    st.session_state.selected_job_id = None

# --- Fetch job listings from Supabase ---
response = supabase.table("job_description") \
    .select("job_id, job_title, date_posted, description") \
    .order("date_posted", desc=True) \
    .execute()
jobs = response.data

# --- Layout: 2 columns ---
col1, col2 = st.columns([1, 2])

# --- LEFT: Job Titles + Dates ---
with col1:
    st.markdown("### 📋 Job Listings")
    for job in jobs:
        job_label = f"**{job['job_title']}**  \n🗓️ *Posted: {job['date_posted']}*"
        if st.button(job_label, key=job["job_id"]):
            st.session_state.selected_job_id = job["job_id"]

# --- RIGHT: Job Details ---
with col2:
    if st.session_state.selected_job_id:
        selected_job = next((j for j in jobs if j["job_id"] == st.session_state.selected_job_id), None)
        if selected_job:
            st.markdown(f"## {selected_job['job_title']}")
            st.markdown(f"📅 **Posted on:** {selected_job['date_posted']}")
            st.markdown("---")
            st.markdown(selected_job["description"], unsafe_allow_html=True)
            st.markdown("---")
            st.button("✅ Apply Now")  # ← static for now
        else:
            st.warning("Could not load job description.")
    else:
        st.info("⬅️ Click a job title to see the full description.")
