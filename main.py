import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key="AIzaSyArNjAreog5Ls4S-O2X9OZk7EYoHstqP1Q")  # Replace with your actual API key
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

app = FastAPI()

# Input model
class JobInput(BaseModel):
    job_title: str
    custom_note: str
    key_focus: str
    benefits: str = ""  # Optional but expected string

@app.post("/generate-job-description")
async def generate_job_description(data: JobInput):
    try:
        # Construct the prompt with all inputs
        prompt = f"""
Generate a detailed and professional job description for a **{data.job_title}** role. Follow this exact structure and include realistic and specific content:

1. **About the Job** section: Include this note – "{data.custom_note}".

2. **Required Skills** section: Include 10–12 highly specific technical and soft skills related to {data.key_focus}. Use bullet points and mention tools, technologies, or techniques where appropriate.

3. **Featured Benefits** section: Include the following benefits as bullet points:
{data.benefits}

Use section headings: "About the Job", "Required Skills", and "Featured Benefits". Keep the tone professional, structured, and suitable for a U.S.-based tech company.
"""

        # Generate job description using Gemini
        response = model.generate_content(prompt)
        return {"job_description": response.text}

    except Exception as e:
        print("❌ Gemini error:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Gemini API failed. See server logs.")
