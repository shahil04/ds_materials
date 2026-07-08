import os
from dotenv import load_dotenv
load_dotenv()
import json
import requests
from datetime import datetime
# from anthropic import Anthropic
from tavily import TavilyClient

_anthropic_client = None
_tavily_client = None

# def get_anthropic_client():
#     global _anthropic_client
#     if _anthropic_client is None:
#         _anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
#     return _anthropic_client
from openai import OpenAI
import os

_openai_client = None

def get_openai_client():
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _openai_client

def get_tavily_client():
    global _tavily_client
    if _tavily_client is None:
        _tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    return _tavily_client

def get_system_prompt(resume_text=None):
    base_prompt = """You are a Job Hunter Agent. Your job is to help users find relevant job listings and prepare application materials.

When a user gives you a job search query, you follow this process:

STEP 0 - ANALYZE INTENT: If the user says something like "find jobs based on my resume" or "find jobs matching my skills" WITHOUT specifying a particular role, first use the extract_resume_keywords tool to identify their key skills, job titles, and industries from their resume. Then use those keywords to make 2-3 different search_jobs calls targeting different angles. If the user asks for a SPECIFIC role (like "find me AI engineer jobs"), skip this step and search directly.

STEP 1 - SEARCH: Use the search_jobs tool to find relevant job listings. If you extracted keywords from the resume, make 2-3 searches using different keyword combinations for broader coverage.

STEP 2 - READ: For the top 3-5 most promising results across all searches, use the read_job_posting tool to fetch the full job description from each URL. Skip URLs that look like job aggregator homepages.

STEP 3 - SCORE: For each job you successfully read, use the score_job_match tool to score it against the user's resume/profile.

STEP 4 - REPORT: Present a final ranked briefing. For EACH job include:
  - Job title and company
  - Link to the job posting (the actual URL)
  - Match score and why it's a good/bad fit
  - Key requirements from the posting
  - A short personalized cover letter draft (3-4 sentences)

IMPORTANT RULES:
- Always include the job posting URL/link for every job in the report.
- Always search first, then read, then score. Don't skip steps.
- If a URL fails to load, skip it and move to the next one.
- Be honest about match scores - don't inflate them.
- If no resume has been uploaded, tell the user to upload their resume as a PDF.
"""
    if resume_text:
        base_prompt += f"\nUSER'S RESUME:\n---\n{resume_text}\n---\nUse this resume for scoring and cover letters.\n"
    else:
        base_prompt += "\nNOTE: No resume uploaded yet. Tell the user to upload their resume as a PDF.\n"
    return base_prompt

TOOLS = [
    {
        "name": "extract_resume_keywords",
        "description": "Extract key skills, job titles, and industries from the user's resume to generate smart job search queries. Use this FIRST when the user asks to find jobs based on my resume without specifying a particular role.",
        "input_schema": {
            "type": "object",
            "properties": {
                "skills": {"type": "array", "items": {"type": "string"}, "description": "Key skills from the resume"},
                "job_titles": {"type": "array", "items": {"type": "string"}, "description": "Relevant job titles based on experience"},
                "industries": {"type": "array", "items": {"type": "string"}, "description": "Industries suited for"},
                "experience_level": {"type": "string", "description": "junior, mid, senior, lead"}
            },
            "required": ["skills", "job_titles"]
        }
    },
    {
        "name": "search_jobs",
        "description": "Search the web for job listings matching a query. Returns titles, snippets, and URLs.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The job search query"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "read_job_posting",
        "description": "Fetch and read the full content of a job posting from its URL.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL of the job posting to read"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "score_job_match",
        "description": "Score how well a job matches the user's resume. Returns a score out of 100.",
        "input_schema": {
            "type": "object",
            "properties": {
                "job_title": {"type": "string"},
                "company": {"type": "string"},
                "required_skills": {"type": "array", "items": {"type": "string"}},
                "user_skills": {"type": "array", "items": {"type": "string"}},
                "nice_to_have_skills": {"type": "array", "items": {"type": "string"}},
                "seniority_level": {"type": "string"},
                "remote_friendly": {"type": "boolean"},
                "job_type": {"type": "string"}
            },
            "required": ["job_title", "company", "required_skills", "user_skills"]
        }
    },
    {
        "name": "get_datetime",
        "description": "Get the current date and time.",
        "input_schema": {"type": "object", "properties": {}, "required": []}
    }
]

def extract_resume_keywords(skills, job_titles, industries=None, experience_level="mid"):
    search_queries = []
    for title in job_titles[:3]:
        search_queries.append(f"{title} remote 2026")
    if skills:
        top_skills = " ".join(skills[:3])
        search_queries.append(f"{top_skills} developer jobs remote")
    if industries:
        for industry in industries[:2]:
            search_queries.append(f"{job_titles[0] if job_titles else 'developer'} {industry} jobs")
    return json.dumps({"skills": skills, "job_titles": job_titles, "industries": industries or [], "experience_level": experience_level, "suggested_search_queries": search_queries}, indent=2)

def search_jobs(query):
    try:
        results = get_tavily_client().search(query=query + " job listing hiring", max_results=8, search_depth="advanced")
        formatted = []
        for r in results.get("results", []):
            formatted.append({"title": r.get("title", "No title"), "url": r.get("url", ""), "snippet": r.get("content", "")[:300]})
        return json.dumps(formatted, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Search failed: {str(e)}"})

def read_job_posting(url):
    try:
        result = get_tavily_client().extract(urls=[url])
        if result and result.get("results"):
            content = result["results"][0].get("raw_content", "")
            if len(content) > 4000:
                content = content[:4000] + "\n\n[Content truncated...]"
            return content if content else "Could not extract content from this URL."
        return "Could not extract content from this URL."
    except Exception as e:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(url, headers=headers, timeout=10)
            return resp.text[:4000]
        except Exception as e2:
            return f"Failed to read URL: {str(e2)}"

def score_job_match(job_title, company, required_skills, user_skills, nice_to_have_skills=None, seniority_level="mid", remote_friendly=True, job_type="full-time"):
    user_skills_lower = {s.lower().strip() for s in user_skills}
    required_lower = [s.lower().strip() for s in required_skills]
    matched_required, missing_required = [], []
    for skill in required_lower:
        if any(us in skill or skill in us for us in user_skills_lower):
            matched_required.append(skill)
        else:
            missing_required.append(skill)
    nice_to_have_skills = nice_to_have_skills or []
    nice_lower = [s.lower().strip() for s in nice_to_have_skills]
    matched_nice = [s for s in nice_lower if any(us in s or s in us for us in user_skills_lower)]
    skill_score = (len(matched_required) / max(len(required_lower), 1)) * 50
    nice_score = (len(matched_nice) / max(len(nice_lower), 1)) * 15 if nice_lower else 10
    seniority_scores = {"junior": 15, "entry": 15, "mid": 12, "mid-level": 12, "senior": 5, "lead": 3, "principal": 2, "staff": 3}
    seniority_score = seniority_scores.get(seniority_level.lower(), 8)
    remote_score = 10 if remote_friendly else 5
    type_scores = {"contract": 10, "freelance": 10, "full-time": 8, "part-time": 7}
    type_score = type_scores.get(job_type.lower(), 7)
    total = min(round(skill_score + nice_score + seniority_score + remote_score + type_score), 100)
    return json.dumps({"score": total, "job_title": job_title, "company": company, "matched_skills": matched_required + matched_nice, "missing_skills": missing_required, "seniority_fit": seniority_level, "remote": remote_friendly, "breakdown": {"skills_match": round(skill_score), "nice_to_have": round(nice_score), "seniority_fit": seniority_score, "remote_fit": remote_score, "job_type_fit": type_score}}, indent=2)

def get_datetime():
    now = datetime.now()
    return json.dumps({"date": now.strftime("%Y-%m-%d"), "time": now.strftime("%H:%M:%S"), "day": now.strftime("%A"), "formatted": now.strftime("%A, %B %d, %Y at %I:%M %p")})

def run_tool(tool_name, tool_input):
    if tool_name == "extract_resume_keywords":
        return extract_resume_keywords(**tool_input)
    elif tool_name == "search_jobs":
        return search_jobs(tool_input["query"])
    elif tool_name == "read_job_posting":
        return read_job_posting(tool_input["url"])
    elif tool_name == "score_job_match":
        return score_job_match(**tool_input)
    elif tool_name == "get_datetime":
        return get_datetime()
    else:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})

def run_agent(user_message, conversation_history=None, resume_text=None):
    if conversation_history is None:
        conversation_history = []
    conversation_history.append({"role": "user", "content": user_message})
    system_prompt = get_system_prompt(resume_text)

    messages = [{"role": "system", "content": system_prompt}]
    for msg in conversation_history:
        if msg["role"] in ["user", "assistant"]:
            messages.append({"role": msg["role"], "content": msg["content"]})

    response = get_openai_client().chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1200,
        temperature=0.7
    )

    assistant_message = response.choices[0].message["content"].strip()
    conversation_history.append({"role": "assistant", "content": assistant_message})
    return assistant_message

if __name__ == "__main__":
    print("Job Hunter Agent - Terminal Mode")
    print("Type your job search query (or 'quit' to exit)")
    history = []
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            break
        if not user_input:
            continue
        print("\nThinking...\n")
        response = run_agent(user_input, history)
        print(f"\nAgent:\n{response}")