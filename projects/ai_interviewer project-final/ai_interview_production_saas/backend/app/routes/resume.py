# ==================================================
# AI Resume Analyzer – Single File FastAPI Backend
# ==================================================

from fastapi import FastAPI, UploadFile, File
import pdfplumber
import spacy
from spacy.cli import download

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading en_core_web_sm model...")
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

import re
import os
import time
import json
from dotenv import load_dotenv
from pathlib import Path
from huggingface_hub import InferenceClient
from pathlib import Path

# Explicitly load .env from backend/app/.env (where user is editing) AND backend/.env
# override=True ensures that even if the system has a variable, we take the one from the file
current_file_path = Path(__file__).resolve()
app_env_path = current_file_path.parent.parent / ".env" # backend/app/.env
root_env_path = current_file_path.parent.parent.parent / ".env" # backend/.env

# Try loading from app dir first (higher priority if user is editing this one)
if app_env_path.exists():
    load_dotenv(dotenv_path=app_env_path, override=True)
# Then try loading from root dir (as fallback or if that's where they put it)
elif root_env_path.exists():
    load_dotenv(dotenv_path=root_env_path, override=True)
else:
    # Fallback to default search
    load_dotenv(override=True)

try:
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not hf_token:
        print("CRITICAL WARNING: HUGGINGFACEHUB_API_TOKEN not found! Please add it to your .env file.")
        client = None
    else:
        print(f"Loaded HUGGINGFACEHUB_API_TOKEN: {hf_token[:4]}...{hf_token[-4:]}")
        client = InferenceClient(api_key=hf_token)
except Exception as e:
    print(f"Warning: Hugging Face Client configuration failed: {e}")
    client = None
# ==================================================
# JOB MATCHER (removed)
# ==================================================
# Code related to jobs.csv removed as per user request


# ==================================================
# CONSTANTS
# ==================================================

COMMON_SKILLS = {
    "python","sql","excel","tableau","power bi","data analysis",
    "machine learning","ai","statistics","communication",
    "project management"
}

# ==================================================
# TEXT CLEANER
# ==================================================

def clean_resume_text(text: str) -> str:
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    text = re.sub(r"\.(\w)", r". \1", text)
    text = re.sub(r"[^a-zA-Z0-9.,:;@()\-\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ==================================================
# PDF TEXT EXTRACTION
# ==================================================

def extract_pdf_text(uploaded_file) -> str:
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# ==================================================
# RESUME PARSER
# ==================================================

def extract_skills(text: str):
    text = text.lower()
    return list({skill for skill in COMMON_SKILLS if skill in text})

def extract_entities(text: str):
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        entities.setdefault(ent.label_, []).append(ent.text)
    return entities

def extract_info(text: str) -> dict:
    cleaned = clean_resume_text(text)
    return {
        "skills": extract_skills(cleaned),
        "entities": extract_entities(cleaned)
    }

# ==================================================
# LOCAL ATS SCORE (HEURISTIC)
# ==================================================

def local_ats_score(resume_text: str) -> int:
    words = resume_text.split()
    length_score = 1 if 200 <= len(words) <= 800 else 0.6
    skill_score = min(len(extract_skills(resume_text)) / 8, 1)
    return int((0.6 * length_score + 0.4 * skill_score) * 100)

# ==================================================
# HUGGING FACE AI ADVICE
# ==================================================

def get_ai_advice(info: dict, job_role: str = "", job_description: str = "") -> dict:
    if not client:
        return {"analysis": "Error: Hugging Face Token is missing. Please check your .env file."}

    base_info = f"""
    Resume Skills: {', '.join(info.get('skills', []))}
    Entities: {info.get('entities', {})}
    """

    if job_role and job_description:
        system_prompt = "You are an expert ATS (Applicant Tracking System) and Recruiter. You must output ONLY valid JSON."
        user_prompt = f"""
        Analyze this resume against the job description.
        
        {base_info}

        Target Job Role: {job_role}
        Target Job Description:
        {job_description}

        Output strictly valid JSON with this structure (no markdown, no extra text):
        {{
            "match_percentage": <int 0-100>,
            "missing_keywords": [<list of strings>],
            "strengths": [<list of concise strings>],
            "weaknesses": [<list of concise strings>],
            "interview_questions": [<list of 5 tailored questions>],
            "hiring_recommendation": "<string>",
            "analysis": "<detailed analysis text>"
        }}
        """
        
        content = ""
        try:
            response = client.chat_completion(
                model="mistralai/Mistral-7B-Instruct-v0.3",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            content = response.choices[0].message.content
            
            # Cleaning cleanup for JSON
            content = content.replace("```json", "").replace("```", "").strip()
            # Sometimes models add text before/after
            start_idx = content.find("{")
            end_idx = content.rfind("}") + 1
            if start_idx != -1 and end_idx != -1:
                content = content[start_idx:end_idx]

            return json.loads(content)
        except Exception as e:
            print(f"HF Error: {e}")
            return {
                "match_percentage": 0,
                "missing_keywords": [],
                "strengths": [],
                "weaknesses": [],
                "interview_questions": [],
                "analysis": f"Error parsing AI response: {e}. Raw content: {content[:100]}...",
                "hiring_recommendation": "Error"
            }

    else:
        # General Advice (Chat)
        user_prompt = f"""
        {base_info}
        Give clear career suggestions and next steps based on these skills.
        """
        try:
            response = client.chat_completion(
                model="mistralai/Mistral-7B-Instruct-v0.3",
                messages=[{"role": "user", "content": user_prompt}],
                max_tokens=800
            )
            return {"analysis": response.choices[0].message.content}
        except Exception as e:
            return {"analysis": f"Error contacting AI: {e}"}

# ==================================================
# FASTAPI ENDPOINT
# ==================================================

from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter()   # ✅ REQUIRED

@router.post("/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...),
    job_role: str = Form(""),
    job_description: str = Form("")
):
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF resumes are supported"}

    raw_text = extract_pdf_text(file.file)

    if len(raw_text) < 100:
        return {"error": "Could not extract readable resume text"}

    info = extract_info(raw_text)
    
    # If JD is provided, get AI ATS analysis
    ai_result = get_ai_advice(info, job_role, job_description)

    # Calculate local ATS score (heuristic)
    local_score = local_ats_score(raw_text)

    return {
        "ats_score": ai_result.get("match_percentage", local_score), # Use AI score if available
        "local_app_score": local_score,
        "skills": info["skills"],
        "entities": info["entities"],
        "ai_analysis": ai_result.get("analysis", ""),
        "missing_keywords": ai_result.get("missing_keywords", []),
        "strengths": ai_result.get("strengths", []),
        "weaknesses": ai_result.get("weaknesses", []),
        "interview_questions": ai_result.get("interview_questions", []),
        "hiring_recommendation": ai_result.get("hiring_recommendation", ""),
        "job_role": job_role,
        "job_description_snippet": job_description[:50] + "..." if job_description else None
    }

