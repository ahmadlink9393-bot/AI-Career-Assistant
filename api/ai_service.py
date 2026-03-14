import os
import json
from dotenv import load_dotenv
from google import genai

# 1. Initialize environment variables
load_dotenv()

# 2. Get API Key and Validate
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # This will show in your terminal if the .env file isn't read correctly
    raise ValueError("❌ Error: GEMINI_API_KEY not found in .env file")

# 3. Initialize the Google AI Client (2026 Library Version)
client = genai.Client(api_key=api_key)

def analyze_resume(resume_text: str, job_text: str):
    """
    Compares a resume against a job description using Gemini AI.
    Returns a structured JSON object with match analysis.
    """
    
    # Prompt engineering to ensure AI returns strictly valid JSON
    prompt = f"""
    You are an expert HR Recruitment Tool. 
    Compare the following Resume with the Job Description.
    Return ONLY a valid JSON object. Do not include markdown backticks or extra text.
    
    Expected JSON Structure:
    {{
        "match_score": (integer between 0-100),
        "missing_keywords": ["list", "of", "missing", "skills"],
        "advice": "short professional advice for the candidate"
    }}

    Resume: {resume_text}
    Job Description: {job_text}
    """

    try:
        # Generate content using Gemini 1.5 Flash
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Analyze this Resume: {resume_text} against this Job: {job_text}. Return ONLY JSON."
        )
        
        # Clean the response text from any AI formatting markers
        clean_text = response.text.strip()
        if "```json" in clean_text:
            clean_text = clean_text.split("```json")[1].split("```")[0].strip()
        
        # Convert string response to Python dictionary (JSON)
        return json.loads(clean_text)

    except Exception as e:
        print(f"❌ AI Service Error: {e}")
        return {
            "match_score": 0,
            "missing_keywords": [],
            "advice": f"Analysis failed due to a server error: {str(e)}"
        }