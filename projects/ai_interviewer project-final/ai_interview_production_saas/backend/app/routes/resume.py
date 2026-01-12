# ==================================================
# AI Resume Analyzer – Single File FastAPI Backend
# ==================================================

from fastapi import FastAPI, UploadFile, File
import pdfplumber
import spacy
import re
import os
import pandas as pd
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai

# ==================================================
# ENV + MODEL SETUP
# ==================================================

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))

nlp = spacy.load("en_core_web_sm")

app = FastAPI(
    title="AI Resume Analyzer API",
    version="1.0.0"
)

# ==================================================
# CONSTANTS
# ==================================================

COMMON_SKILLS = {
    "python","sql","excel","tableau","power bi","data analysis",
    "machine learning","ai","statistics","communication",
    "project management","marketing","sales","legal research"
}
# common skills generate from based on job role and job descriptions  common skill variable
# or also extract the skills from resume for ATS score  and store resume skill variable
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
# JOB MATCHER (TF-IDF)
# ==================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def match_jobs(resume_skills):
    csv_path = os.path.join(BASE_DIR, "..", "data", "jobs.csv")

    if not os.path.exists(csv_path):
        return []

    df = pd.read_csv(csv_path)


    df["combined"] = df["Title"] + " " + df["Skills"]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df["combined"])

    resume_vector = vectorizer.transform([" ".join(resume_skills)])
    df["score"] = cosine_similarity(resume_vector, tfidf_matrix).flatten()

    return df.sort_values("score", ascending=False).head(5).to_dict(orient="records")

# ==================================================
# LOCAL ATS SCORE (HEURISTIC)
# ==================================================

def local_ats_score(resume_text: str) -> int:
    words = resume_text.split()
    length_score = 1 if 200 <= len(words) <= 800 else 0.6
    skill_score = min(len(extract_skills(resume_text)) / 8, 1)
    return int((0.6 * length_score + 0.4 * skill_score) * 100)

# ==================================================
# GEMINI AI ADVICE
# ==================================================

def get_ai_advice(info: dict) -> str:
    prompt = f"""
    Resume Skills:
    {', '.join(info.get('skills', []))}

    Entities:
    {info.get('entities', {})}

    Give clear career suggestions and next steps.
    """

    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

# ==================================================
# FASTAPI ENDPOINT
# ==================================================

from fastapi import APIRouter, UploadFile, File

router = APIRouter()   # ✅ REQUIRED

@router.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF resumes are supported"}

    raw_text = extract_pdf_text(file.file)

    if len(raw_text) < 100:
        return {"error": "Could not extract readable resume text"}

    info = extract_info(raw_text)
    matched_jobs = match_jobs(info["skills"])
    ats_score = local_ats_score(raw_text)
    ai_advice = get_ai_advice(info)

    return {
        "ats_score": ats_score,
        "skills": info["skills"],
        "entities": info["entities"],
        "matched_jobs": matched_jobs,
        "ai_career_suggestions": ai_advice
    }

