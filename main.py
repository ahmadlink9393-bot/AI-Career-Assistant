import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import uvicorn

# Imports for local ML and External AI
from job_matching.matcher import SkillMatcher
from api.ai_service import analyze_resume

# Core API components
from api.database import SessionLocal, engine
from api import models, schemas
from resume_parser.parser import ResumeParser

# Initialize Database Tables
models.Base.metadata.create_all(bind=engine)

# 1. Initialize local Machine Learning Engine (The .pth model user)
# This loads your trained model once when the server starts
matcher = SkillMatcher()

app = FastAPI(
    title="AI Career Assistant Platform",
    description="Professional Portfolio Project for Resume Analysis & ML Matching",
    version="1.0.0"
)

# Database Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 1. Upload Resume (PDF) ---
@app.post("/resumes/upload", response_model=schemas.ResumeResponse)
async def upload_resume(candidate_name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        pdf_content = await file.read()
        # Clean text extraction using PyMuPDF
        extracted_text = ResumeParser.extract_text_from_pdf_bytes(pdf_content)
        
        if not extracted_text:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

        db_resume = models.Resume(candidate_name=candidate_name, content=extracted_text)
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)
        return db_resume
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

# --- 2. Add Job Description ---
@app.post("/jobs/", response_model=schemas.JobDescriptionResponse)
def create_job(job: schemas.JobDescriptionCreate, db: Session = Depends(get_db)):
    db_job = models.JobDescription(title=job.title, description_text=job.description_text)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

# --- 3. Hybrid AI Analysis (Local ML + Gemini) ---
@app.post("/analyze/{resume_id}/{job_id}")
def run_analysis(resume_id: int, job_id: int, db: Session = Depends(get_db)):
    # Fetch records
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    job = db.query(models.JobDescription).filter(models.JobDescription.id == job_id).first()

    if not resume or not job:
        raise HTTPException(status_code=404, detail="Resume or Job not found")

    # A. Execute Local ML Match (Using PyTorch .pth)
    # This gives you a mathematical similarity score
    ml_compatibility_score = matcher.calculate_score(resume.content, job.description_text)

    # B. Execute Generative AI Analysis (Gemini API)
    # This gives you strengths, weaknesses, and suggestions
    gen_ai_results = analyze_resume(resume.content, job.description_text)
    
    # Combine results into one final report
    final_report = {
        "ml_match_score": f"{ml_compatibility_score}%",
        "ai_deep_analysis": gen_ai_results
    }

    # Save results to DB (Ensure JSON column exists in models.py)
    resume.analysis_results = final_report
    db.commit()

    return final_report

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)