import json
import os
from datetime import datetime
from typing import Any

import requests
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from tavily import TavilyClient

load_dotenv()

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
MAX_TOOL_ROUNDS = int(os.getenv("MAX_TOOL_ROUNDS", "8"))

_llm = None
_tavily_client = None


def get_llm():
    global _llm
    if _llm is None:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set.")
        _llm = ChatOpenAI(model=DEFAULT_MODEL, temperature=0.3, max_tokens=1200)
    return _llm


def get_tavily_client():
    global _tavily_client
    if _tavily_client is None:
        if not os.getenv("TAVILY_API_KEY"):
            raise RuntimeError("TAVILY_API_KEY is not set.")
        _tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    return _tavily_client


def get_system_prompt(resume_text=None):
    base_prompt = """You are a Job Hunter Agent. Your job is to help users find relevant job listings and prepare application materials.

When a user gives you a job search query, follow this process:

STEP 0 - ANALYZE INTENT: If the user says something like "find jobs based on my resume" or "find jobs matching my skills" without specifying a particular role, first use the extract_resume_keywords tool to identify their key skills, job titles, and industries from their resume. Then use those keywords to make 2-3 different search_jobs calls targeting different angles. If the user asks for a specific role, like "find me AI engineer jobs", skip this step and search directly.

STEP 1 - SEARCH: Use the search_jobs tool to find relevant job listings. If you extracted keywords from the resume, make 2-3 searches using different keyword combinations for broader coverage.

STEP 2 - READ: For the top 3-5 most promising results across all searches, use the read_job_posting tool to fetch the full job description from each URL. Skip URLs that look like job aggregator homepages.

STEP 3 - SCORE: For each job you successfully read, use the score_job_match tool to score it against the user's resume/profile.

STEP 4 - REPORT: Present a final ranked briefing. For each job include:
- Job title and company
- Link to the job posting
- Match score and why it is a good or weak fit
- Key requirements from the posting
- A short personalized cover letter draft, 3-4 sentences

IMPORTANT RULES:
- Always include the job posting URL/link for every job in the report.
- Always search first, then read, then score.
- If a URL fails to load, skip it and move to the next one.
- Be honest about match scores. Do not inflate them.
- If no resume has been uploaded, tell the user to upload their resume as a PDF.
"""
    if resume_text:
        base_prompt += f"\nUSER'S RESUME:\n---\n{resume_text}\n---\nUse this resume for scoring and cover letters.\n"
    else:
        base_prompt += "\nNOTE: No resume uploaded yet. Tell the user to upload their resume as a PDF.\n"
    return base_prompt


class ExtractResumeKeywordsArgs(BaseModel):
    skills: list[str] = Field(description="Key skills from the resume")
    job_titles: list[str] = Field(description="Relevant job titles based on experience")
    industries: list[str] | None = Field(default=None, description="Suitable industries")
    experience_level: str = Field(default="mid", description="junior, mid, senior, or lead")


class SearchJobsArgs(BaseModel):
    query: str = Field(description="The job search query")


class ReadJobPostingArgs(BaseModel):
    url: str = Field(description="The URL of the job posting to read")


class ScoreJobMatchArgs(BaseModel):
    job_title: str
    company: str
    required_skills: list[str]
    user_skills: list[str]
    nice_to_have_skills: list[str] | None = None
    seniority_level: str = "mid"
    remote_friendly: bool = True
    job_type: str = "full-time"


class EmptyArgs(BaseModel):
    pass


def extract_resume_keywords(
    skills: list[str],
    job_titles: list[str],
    industries: list[str] | None = None,
    experience_level: str = "mid",
):
    search_queries = []
    for title in job_titles[:3]:
        search_queries.append(f"{title} remote 2026")

    if skills:
        top_skills = " ".join(skills[:3])
        search_queries.append(f"{top_skills} developer jobs remote")

    if industries:
        for industry in industries[:2]:
            title = job_titles[0] if job_titles else "developer"
            search_queries.append(f"{title} {industry} jobs")

    return json.dumps(
        {
            "skills": skills,
            "job_titles": job_titles,
            "industries": industries or [],
            "experience_level": experience_level,
            "suggested_search_queries": search_queries,
        },
        indent=2,
    )


def search_jobs(query: str):
    try:
        results = get_tavily_client().search(
            query=f"{query} job listing hiring",
            max_results=8,
            search_depth="advanced",
        )
        formatted = [
            {
                "title": item.get("title", "No title"),
                "url": item.get("url", ""),
                "snippet": item.get("content", "")[:300],
            }
            for item in results.get("results", [])
        ]
        return json.dumps(formatted, indent=2)
    except Exception as exc:
        return json.dumps({"error": f"Search failed: {exc}"})


def read_job_posting(url: str):
    try:
        result = get_tavily_client().extract(urls=[url])
        if result and result.get("results"):
            content = result["results"][0].get("raw_content", "")
            if len(content) > 4000:
                content = f"{content[:4000]}\n\n[Content truncated...]"
            return content if content else "Could not extract content from this URL."
        return "Could not extract content from this URL."
    except Exception:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text[:4000]
        except Exception as exc:
            return f"Failed to read URL: {exc}"


def score_job_match(
    job_title: str,
    company: str,
    required_skills: list[str],
    user_skills: list[str],
    nice_to_have_skills: list[str] | None = None,
    seniority_level: str = "mid",
    remote_friendly: bool = True,
    job_type: str = "full-time",
):
    user_skills_lower = {skill.lower().strip() for skill in user_skills}
    required_lower = [skill.lower().strip() for skill in required_skills]

    matched_required = []
    missing_required = []
    for skill in required_lower:
        if any(user_skill in skill or skill in user_skill for user_skill in user_skills_lower):
            matched_required.append(skill)
        else:
            missing_required.append(skill)

    nice_to_have_skills = nice_to_have_skills or []
    nice_lower = [skill.lower().strip() for skill in nice_to_have_skills]
    matched_nice = [
        skill
        for skill in nice_lower
        if any(user_skill in skill or skill in user_skill for user_skill in user_skills_lower)
    ]

    skill_score = (len(matched_required) / max(len(required_lower), 1)) * 50
    nice_score = (len(matched_nice) / max(len(nice_lower), 1)) * 15 if nice_lower else 10

    seniority_scores = {
        "junior": 15,
        "entry": 15,
        "mid": 12,
        "mid-level": 12,
        "senior": 5,
        "lead": 3,
        "principal": 2,
        "staff": 3,
    }
    seniority_score = seniority_scores.get(seniority_level.lower(), 8)
    remote_score = 10 if remote_friendly else 5
    type_scores = {"contract": 10, "freelance": 10, "full-time": 8, "part-time": 7}
    type_score = type_scores.get(job_type.lower(), 7)
    total = min(round(skill_score + nice_score + seniority_score + remote_score + type_score), 100)

    return json.dumps(
        {
            "score": total,
            "job_title": job_title,
            "company": company,
            "matched_skills": matched_required + matched_nice,
            "missing_skills": missing_required,
            "seniority_fit": seniority_level,
            "remote": remote_friendly,
            "breakdown": {
                "skills_match": round(skill_score),
                "nice_to_have": round(nice_score),
                "seniority_fit": seniority_score,
                "remote_fit": remote_score,
                "job_type_fit": type_score,
            },
        },
        indent=2,
    )


def get_datetime():
    now = datetime.now()
    return json.dumps(
        {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "day": now.strftime("%A"),
            "formatted": now.strftime("%A, %B %d, %Y at %I:%M %p"),
        }
    )


TOOLS = [
    StructuredTool.from_function(
        func=extract_resume_keywords,
        name="extract_resume_keywords",
        description=(
            "Extract key skills, job titles, and industries from the user's resume to generate "
            "smart job search queries. Use first when the user asks to find jobs based on a resume "
            "without naming a specific role."
        ),
        args_schema=ExtractResumeKeywordsArgs,
    ),
    StructuredTool.from_function(
        func=search_jobs,
        name="search_jobs",
        description="Search the web for job listings matching a query. Returns titles, snippets, and URLs.",
        args_schema=SearchJobsArgs,
    ),
    StructuredTool.from_function(
        func=read_job_posting,
        name="read_job_posting",
        description="Fetch and read the full content of a job posting from its URL.",
        args_schema=ReadJobPostingArgs,
    ),
    StructuredTool.from_function(
        func=score_job_match,
        name="score_job_match",
        description="Score how well a job matches the user's resume. Returns a score out of 100.",
        args_schema=ScoreJobMatchArgs,
    ),
    StructuredTool.from_function(
        func=get_datetime,
        name="get_datetime",
        description="Get the current date and time.",
        args_schema=EmptyArgs,
    ),
]

TOOL_BY_NAME = {tool.name: tool for tool in TOOLS}


def _history_to_messages(conversation_history: list[dict[str, Any]]) -> list[BaseMessage]:
    messages: list[BaseMessage] = []
    for item in conversation_history:
        role = item.get("role")
        content = item.get("content", "")
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))
    return messages


def _content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                parts.append(str(item.get("text", item)))
            else:
                parts.append(str(item))
        return "\n".join(parts)
    return str(content or "")


def run_tool(tool_name: str, tool_input: dict[str, Any]):
    tool = TOOL_BY_NAME.get(tool_name)
    if tool is None:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})
    try:
        return tool.invoke(tool_input)
    except Exception as exc:
        return json.dumps({"error": f"Tool {tool_name} failed: {exc}"})


def run_agent(user_message, conversation_history=None, resume_text=None):
    if conversation_history is None:
        conversation_history = []

    conversation_history.append({"role": "user", "content": user_message})

    messages: list[BaseMessage] = [
        SystemMessage(content=get_system_prompt(resume_text)),
        *_history_to_messages(conversation_history),
    ]

    model = get_llm().bind_tools(TOOLS)

    for _ in range(MAX_TOOL_ROUNDS):
        ai_message = model.invoke(messages)
        messages.append(ai_message)

        tool_calls = getattr(ai_message, "tool_calls", None) or []
        if not tool_calls:
            assistant_content = _content_to_text(ai_message.content)
            conversation_history.append({"role": "assistant", "content": assistant_content})
            return assistant_content

        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call.get("args") or {}
            print(f"  Calling tool: {tool_name}")
            tool_result = run_tool(tool_name, tool_args)
            messages.append(
                ToolMessage(
                    content=_content_to_text(tool_result),
                    tool_call_id=tool_call["id"],
                    name=tool_name,
                )
            )

    fallback = "I reached the maximum number of tool steps before finishing. Please try a narrower job search query."
    conversation_history.append({"role": "assistant", "content": fallback})
    return fallback


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
