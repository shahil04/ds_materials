

from utils.resume_parser import extract_info    
from utils.job_matcher import match_jobs  
from utils.ai_suggester import get_ai_advice 
from utils.cleaner import clean_resume_text 
import streamlit as st 
import pdfplumber 
import spacy



# import google.generativeai as genai

# # Configure API key (note: hardcoding API keys is generally not recommended for security)
# genai.configure(api_key="AIzaSyC4CAcWBzlc9NkzFXMirRT4jjVs0dHwe6s")

# # List available models to find a working one
# print("Available Models:")
# for m in genai.list_models():
#     if "generateContent" in m.supported_generation_methods:
#         print(m.name)

# # Load model - Placeholder until a working model is identified from the list above
# model = genai.GenerativeModel("gemini-2.5-flash")

# print("Chat with Google GenAI (Gemini)")

# user_input = "Tell me a joke about AI"
# if user_input:
#     response = model.generate_content(user_input)
#     print("Gemini:", response.text)


# Load the English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")



#==================================================
import google.generativeai as genai
import os
from google.generativeai import configure
# clear.py 

import re

def clean_resume_text(text: str) -> str:
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)         # Separate camelCase words
    text = re.sub(r"[^\x00-\x7F]+", " ", text)               # Remove non-ASCII
    text = re.sub(r"\.(\w)", r". \1", text)                  # Add space after periods
    text = re.sub(r"[^a-zA-Z0-9.,:;@()\-\s]", " ", text)     # Remove unwanted characters
    text = re.sub(r"\s+", " ", text)                         # Collapse multiple spaces
    return text.strip()
# ======================
# job matcher 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_jobs(resume_skills):
    df = pd.read_csv("jobs.csv")

    # Debug print (optional)
    print("CSV Columns:", df.columns.tolist())

    # Ensure the columns exist
    if "Title" not in df.columns or "Skills" not in df.columns:
        raise ValueError("CSV must contain 'Title' and 'Skills' columns.")

    df["combined"] = df["Title"] + " " + df["Skills"]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df["combined"])

    resume_text = " ".join(resume_skills)
    resume_vector = vectorizer.transform([resume_text])

    similarity_scores = cosine_similarity(resume_vector, tfidf_matrix).flatten()
    df["score"] = similarity_scores

    matched = df.sort_values(by="score", ascending=False).head(5)
    return matched[["Title", "Skills", "score"]]

# =====================
# job.csv 
# here the job list which is similar to user job type  create from ai or if not generate use 
# Title	Skills	Company	Location
# Data Analyst	Python, SQL, Excel, Power BI, Tableau, AI, ML	DataCorp	Remote
# Marketing Executive	SEO, Google Ads, Communication, Sales	AdMedia	Bangalore
# Software Developer	Java, Pyhton, SQL, Git, GitHub, Full Stack Web Development	CodeNest	Delhi
# HR Manager	Recruitment, Onboarding, Excel, Communication, Data-Analysis	PeopleTree	Mumbai
# Legal Intern	Legal, Research, Contract Law, CorporateLaw	LawNet	Remote
#=======================================
# resume_parser.py

import spacy
from .cleaner import clean_resume_text  # ✅ Ensure cleaner.py exists and has clean_resume_text

import subprocess
import importlib.util

# Automatically download the model if not present
model_name = "en_core_web_sm"
if not importlib.util.find_spec(model_name):
    subprocess.run(["python", "-m", "spacy", "download", model_name])

# Now import
import en_core_web_sm
nlp = en_core_web_sm.load()

# ✅ Define common skills for matching
COMMON_SKILLS = {
    "python", "sql", "excel", "tableau", "power bi", "data analysis", "machine learning",
    "teamwork", "communication", "leadership", "financial analysis", "problem solving",
    "marketing", "project management", "graphic design", "html", "css", "javascript", 
    "sales", "negotiation", "customer service", "biotechnology", "chemistry", 
    "legal research", "contract law", "data visualization", "statistics", "teaching",
    "counseling", "ai", "creativity", "networking", "public speaking", "presentation"
}

# ✅ Extract matched skills
def extract_skills(text: str):
    text = text.lower()
    return list({skill for skill in COMMON_SKILLS if skill in text})

# ✅ Extract named entities using spaCy
def extract_entities(text: str):
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        label = ent.label_
        value = ent.text.strip()
        if value not in entities.get(label, []):
            entities.setdefault(label, []).append(value)
    return entities

# ✅ Main wrapper function used in app.py
def extract_info(text: str) -> dict:
    cleaned = clean_resume_text(text)
    return {
        "skills": extract_skills(cleaned),
        "entities": extract_entities(cleaned)
    }
# # =======================
# Load environment variables from .env
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the API key
api_key = os.getenv("GOOGLE_GENAI_API_KEY")
genai.configure(api_key=api_key)


def get_ai_advice(info: dict) -> str:
    prompt = f"""
    I'm sharing the following resume information:

    Skills:
    {', '.join(info.get('skills', []))}

    Entities / Experience:
    {', '.join(info.get('entities', []))}

    Based on the above, give me AI-generated career suggestions.
    """
    
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
# ==============================================
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("📄 AI Resume Analyzer & Job Matcher")

uploaded = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded:
    with pdfplumber.open(uploaded) as pdf:
        text = "".join([page.extract_text() or "" for page in pdf.pages])
    st.subheader("📃 Resume Preview")
    st.text(text[:1000])

    cleaned_text = clean_resume_text(text)
    info = extract_info(cleaned_text)

    st.subheader("🧠 Extracted Skills & Info")
    st.json(info)

    jobs = match_jobs(info["skills"])
    st.subheader("🎯 Matched Jobs")
    st.dataframe(jobs)

    st.subheader("🤖 AI Career Suggestions")
    suggestion = get_ai_advice(info)
    st.markdown(suggestion)