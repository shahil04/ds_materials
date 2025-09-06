"""
Streamlit Resume, LinkedIn & GitHub Analyzer
------------------------------------------------
Features:
- Upload resume (PDF, DOCX, TXT). Extract text and analyze.
- Paste job description / role keywords to compare against resume.
- Detect LinkedIn & GitHub URLs and give recommendations.
- Provide an overall "profile readiness" score with section-level breakdown.
- Produce downloadable feedback report.

Notes / Requirements:
- Uses: streamlit, PyPDF2, docx2txt, pandas, sklearn (optional: for better text matching)
- Install (if needed): pip install streamlit PyPDF2 python-docx docx2txt
- This app uses simple, explainable heuristics — easy to extend.

"""

import streamlit as st
import re
import io
import base64
from collections import Counter

try:
    import PyPDF2
except Exception:
    PyPDF2 = None

try:
    import docx2txt
except Exception:
    docx2txt = None

# --------------------------------------------------
# Utility functions
# --------------------------------------------------

SKILLS_DB = [
    # common data science / ML skills (can be extended)
    'python','pandas','numpy','scikit-learn','sklearn','tensorflow','pytorch',
    'sql','excel','power bi','tableau','matplotlib','seaborn','nlp','computer vision',
    'regression','classification','clustering','random forest','xgboost','lightgbm',
    'git','github','docker','aws','gcp','azure','bigquery','spark','hadoop'
]

SECTION_HEADERS = [
    'experience','education','projects','skills','certifications','summary','objective','publications','contact'
]

URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')
EMAIL_PATTERN = re.compile(r'[\w\.-]+@[\w\.-]+')
PHONE_PATTERN = re.compile(r'(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3}\)?[\s-]?|\d{3}[\s-]?)\d{3}[\s-]?\d{4}')
LINKEDIN_PATTERN = re.compile(r'(?:https?://)?(?:www\.)?linkedin\.com/\S+', re.IGNORECASE)
GITHUB_PATTERN = re.compile(r'(?:https?://)?(?:www\.)?github\.com/\S+', re.IGNORECASE)


def extract_text_from_pdf(file_stream):
    if PyPDF2 is None:
        return ""  # PyPDF2 not installed
    try:
        reader = PyPDF2.PdfReader(file_stream)
        text = []
        for page in reader.pages:
            page_text = page.extract_text() or ''
            text.append(page_text)
        return '\n'.join(text)
    except Exception as e:
        return ""


def extract_text_from_docx(file_stream):
    if docx2txt is None:
        return ""
    try:
        # docx2txt expects a path-like object; write to buffer
        tmp = file_stream.read()
        # write to temp file
        with open('/tmp/temp_resume.docx', 'wb') as f:
            f.write(tmp)
        text = docx2txt.process('/tmp/temp_resume.docx')
        return text
    except Exception as e:
        return ""


def extract_text_from_txt(file_stream):
    try:
        raw = file_stream.read()
        if isinstance(raw, bytes):
            raw = raw.decode('utf-8', errors='ignore')
        return raw
    except Exception:
        return ""


def clean_and_tokenize(text):
    t = text.lower()
    # remove punctuation (simple)
    t = re.sub(r'[^a-z0-9\s]', ' ', t)
    tokens = [w for w in t.split() if len(w) > 1]
    return tokens


def detect_sections(text):
    text_lower = text.lower()
    found = {}
    for sec in SECTION_HEADERS:
        if sec in text_lower:
            found[sec] = True
        else:
            found[sec] = False
    return found


def score_skills(tokens, skills_db=SKILLS_DB):
    token_set = set(tokens)
    found = [s for s in skills_db if s.lower() in ' '.join(tokens)]
    # Also count occurrences
    counts = Counter(tokens)
    skill_counts = {s: counts[s] for s in token_set if s in skills_db}
    return found


def simple_keyword_match(resume_text, jd_text):
    resume_tokens = set(clean_and_tokenize(resume_text))
    jd_tokens = set(clean_and_tokenize(jd_text))
    common = resume_tokens.intersection(jd_tokens)
    # focus on skills db intersection too
    skill_overlap = [s for s in SKILLS_DB if s in jd_tokens and s in resume_tokens]
    # Score = proportion of jd tokens present in resume (capped)
    if len(jd_tokens) == 0:
        return 0.0, len(common), skill_overlap
    score = len(common) / len(jd_tokens)
    return round(min(score, 1.0), 3), len(common), skill_overlap


def generate_feedback(resume_text, jd_text=None):
    tokens = clean_and_tokenize(resume_text)
    sections = detect_sections(resume_text)
    skills_found = [s for s in SKILLS_DB if s in resume_text.lower()]

    urls = URL_PATTERN.findall(resume_text)
    emails = EMAIL_PATTERN.findall(resume_text)
    phones = PHONE_PATTERN.findall(resume_text)
    linkedin = LINKEDIN_PATTERN.findall(resume_text)
    github = GITHUB_PATTERN.findall(resume_text)

    # Basic scoring heuristics
    length_words = len(tokens)
    length_score = 1.0 if 200 <= length_words <= 800 else max(0.2, min(1.0, length_words / 800))
    contact_score = 1.0 if (emails or phones) else 0.0
    section_score = sum(1 for v in sections.values() if v) / len(sections)
    skills_score = min(1.0, len(skills_found) / 8)

    overall = round((0.3 * length_score + 0.2 * contact_score + 0.2 * section_score + 0.3 * skills_score) * 100)

    feedback = {
        'overall_score': overall,
        'length_words': length_words,
        'length_score': round(length_score, 2),
        'contact_found': bool(emails or phones),
        'emails': emails,
        'phones': phones,
        'sections': sections,
        'section_score': round(section_score, 2),
        'skills_found': skills_found,
        'skills_score': round(skills_score, 2),
        'linkedin': linkedin,
        'github': github,
        'urls': urls,
    }

    if jd_text:
        jd_score, common_count, skill_overlap = simple_keyword_match(resume_text, jd_text)
        feedback['job_match_score'] = int(jd_score*100)
        feedback['job_common_terms'] = common_count
        feedback['job_skill_overlap'] = skill_overlap
    return feedback


def create_report_text(feedback):
    lines = []
    lines.append(f"Overall Profile Score: {feedback['overall_score']} / 100")
    lines.append(f"Resume length (words): {feedback['length_words']}")
    lines.append(f"Contact info present: {'Yes' if feedback['contact_found'] else 'No'}")
    if feedback['emails']:
        lines.append(f"Emails found: {', '.join(feedback['emails'])}")
    if feedback['phones']:
        lines.append(f"Phones found: {', '.join(feedback['phones'])}")
    lines.append(f"Sections detected (sample): {', '.join([k for k,v in feedback['sections'].items() if v])}")
    lines.append(f"Skills found: {', '.join(feedback['skills_found']) if feedback['skills_found'] else 'None detected'}")
    if 'job_match_score' in feedback:
        lines.append(f"Job Match Score: {feedback['job_match_score']} / 100")
        lines.append(f"Job common term count: {feedback['job_common_terms']}")
        lines.append(f"Job skill overlap: {', '.join(feedback['job_skill_overlap']) if feedback['job_skill_overlap'] else 'None'}")
    lines.append('')
    lines.append('Suggestions:')
    if not feedback['contact_found']:
        lines.append('- Add a professional email and phone number at top (contact section).')
    if feedback['length_words'] < 150:
        lines.append('- Add more detail: brief bullets for projects and impact (metrics).')
    if not feedback['skills_found']:
        lines.append('- Add a Skills section with relevant technologies and tools.')
    if not feedback['linkedin']:
        lines.append('- Add LinkedIn URL in header of resume and LinkedIn profile should be complete.')
    if not feedback['github']:
        lines.append('- Add GitHub link and pin 2-3 projects with README.')
    if feedback.get('job_match_score', 0) < 60:
        lines.append('- Tailor resume for the job: include keywords from the job description.')
    lines.append('- Keep resume to 1 page for freshers, 1-2 pages for experienced professionals.')
    return '\n'.join(lines)

# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------

st.set_page_config(page_title='Resume & Profile Analyzer', layout='wide')
st.title('Resume, LinkedIn & GitHub Analyzer (Interactive)')
st.markdown('Upload your resume (PDF/DOCX/TXT) and paste a job description to get instant feedback and a downloadable report.')

col1, col2 = st.columns([1,2])

with col1:
    uploaded_file = st.file_uploader('Upload Resume', type=['pdf','docx','txt'])
    jd_text = st.text_area('Paste Job Description / Role Keywords (optional)', height=200)
    analyze_btn = st.button('Analyze Resume')

with col2:
    st.info('Tips: Use a clear one-page resume (freshers). Include contact, skills, projects, and links to LinkedIn/GitHub.')
    st.subheader('Sample Skills (Data Science):')
    st.write(', '.join(SKILLS_DB))

resume_text = ''
if uploaded_file is not None:
    file_details = {'filename': uploaded_file.name, 'type': uploaded_file.type}
    st.write('Uploaded:', file_details['filename'])
    # read stream
    if uploaded_file.type == 'application/pdf' or uploaded_file.name.lower().endswith('.pdf'):
        resume_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.lower().endswith('.docx'):
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        resume_text = extract_text_from_txt(uploaded_file)

if analyze_btn:
    if not resume_text:
        st.error('No resume text found or file type not supported. Try uploading a PDF or TXT or DOCX (with python-docx/docx2txt installed).')
    else:
        with st.spinner('Analyzing...'):
            feedback = generate_feedback(resume_text, jd_text)

        # Display
        st.metric('Overall Score', f"{feedback['overall_score']} / 100")
        st.write('---')
        st.subheader('Quick Insights')
        cols = st.columns(3)
        cols[0].write(f"**Words**: {feedback['length_words']}")
        cols[1].write(f"**Sections detected**: {', '.join([k for k,v in feedback['sections'].items() if v])}")
        cols[2].write(f"**Skills found**: {', '.join(feedback['skills_found']) if feedback['skills_found'] else 'None'}")

        st.subheader('Contact & Links')
        st.write(f"Emails: {', '.join(feedback['emails']) if feedback['emails'] else 'None detected'}")
        st.write(f"Phones: {', '.join(feedback['phones']) if feedback['phones'] else 'None detected'}")
        st.write(f"LinkedIn Links: {', '.join(feedback['linkedin']) if feedback['linkedin'] else 'None detected'}")
        st.write(f"GitHub Links: {', '.join(feedback['github']) if feedback['github'] else 'None detected'}")

        if 'job_match_score' in feedback:
            st.subheader('Job Match')
            st.write(f"Job Match Score: {feedback['job_match_score']} / 100")
            st.write(f"Common Terms with Job Description: {feedback['job_common_terms']}")
            st.write(f"Skill Overlap: {', '.join(feedback['job_skill_overlap']) if feedback['job_skill_overlap'] else 'None'}")

        st.subheader('Detailed Feedback & Suggestions')
        report_text = create_report_text(feedback)
        st.text_area('Feedback Report', value=report_text, height=300)

        # Download report
        b = report_text.encode('utf-8')
        href = f"data:file/txt;base64,{base64.b64encode(b).decode()}"
        st.markdown(f"[Download Feedback Report]({href})")

        st.success('Analysis complete. Use suggestions to improve your resume & profile!')

st.markdown('---')
st.caption('Built for learning: extend the skills database, add NLP-based matching, or integrate with LinkedIn/GitHub APIs for richer feedback.')
