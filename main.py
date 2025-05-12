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
Generate a detailed and professional job description for a **{data.job_title}** role at a U.S.-based tech company. Use a tone that is clear, structured, and appealing to experienced professionals, Do not add skills that are not mentioned.
Follow this structure precisely:

1. **About the Job**
   - Start with a 2–3 sentence overview of the role, including the team or department context.
   - Then include this custom note: "{data.custom_note}"
   - Highlight key responsibilities, tools, or impact areas in 3–5 bullet points.

2. **Required Skills**
   - List 10–12 specific technical and soft skills related to **{data.key_focus}**.
   - Include tools, technologies, methodologies, and relevant interpersonal skills.
   - Use bullet points for clarity.

3. **Featured Benefits** section: Include the following benefits as bullet points:
{data.benefits}

Use section headings: "About the Job", "Required Skills", and "Featured Benefits". Keep the tone professional, structured, and suitable for a U.S.-based tech company.
"""

        # Generate job description using Gemini
        response = model.generate_content(prompt)
        return {"job_description": response.text}

    except Exception as e:
        print("Gemini error:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Gemini API failed. See server logs.")
