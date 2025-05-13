import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import datetime
from supabase import create_client, Client

# Load variables from .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY") or "AIzaSyArNjAreog5Ls4S-O2X9OZk7EYoHstqP1Q")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

app = FastAPI()

# Input model for both generation and posting
class JobInput(BaseModel):
    job_title: str
    custom_note: str
    key_focus: str
    benefits: str

class PostJobInput(JobInput):
    job_id: str
    description: str

# --- Endpoint: Generate Job Description ---
@app.post("/generate-job-description")
async def generate_job_description(data: JobInput):
    try:
        prompt = f"""
Generate a detailed and professional job description for a **{data.job_title}** role at a U.S.-based tech company. Use a tone that is clear, structured, and appealing to experienced professionals.

1. **About the Job**
   - Start with a 2–3 sentence overview of the role, including the team or department context.
   - Then include this custom note: "{data.custom_note}"
   - Highlight key responsibilities, tools, or impact areas in 3–5 bullet points.

2. **Required Skills**
   - List 10–12 specific technical and soft skills related to **{data.key_focus}**.
   - Include tools, technologies, methodologies, and relevant interpersonal skills.
   - Use bullet points for clarity.

3. **Featured Benefits**
   - Include the following benefits as bullet points:
{data.benefits}

Use section headings: "About the Job", "Required Skills", and "Featured Benefits".
"""
        response = model.generate_content(prompt)
        return {"job_description": response.text}

    except Exception as e:
        print("Gemini error:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Gemini API failed. See server logs.")

# --- Endpoint: Post to Supabase ---
@app.post("/post-job-description")
async def post_job_description(data: PostJobInput):
    try:
        supabase.table("job_description").insert({
            "job_id": data.job_id,
            "description": data.description,
            "job_title": data.job_title,
            "custom_note": data.custom_note,
            "key_focus": data.key_focus,
            "benefits": data.benefits,
            "date_posted": datetime.utcnow().strftime("%Y-%m-%d")  # ✅ New line
        }).execute()
        return {"status": "success"}
    except Exception as e:
        print("Supabase insert error:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to save to Supabase")
@app.get("/jobs")
async def get_job_listings():
    try:
        response = supabase.table("job_description") \
            .select("job_id, job_code, job_title, date_posted, description") \
            .order("date_posted", desc=True) \
            .execute()
        return response.data
    except Exception as e:
        print("❌ Error fetching jobs:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to retrieve job listings")