import streamlit as st
import pdfplumber
from io import BytesIO
from agent import run_agent

st.set_page_config(page_title="Job Hunter Agent", page_icon="🤖", layout="wide")

st.title("Job Hunter Agent")
st.markdown(
    "Use this Streamlit frontend to upload your resume PDF and ask the agent to find relevant jobs."  
    "The agent uses OpenAI and LangChain for smart job search and matching."
)

if "history" not in st.session_state:
    st.session_state.history = []
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None

with st.sidebar:
    st.header("Resume Upload")
    uploaded_file = st.file_uploader("Upload your resume PDF", type=["pdf"])
    if uploaded_file is not None:
        if st.button("Load Resume"):
            try:
                with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
                    pages = [page.extract_text() or "" for page in pdf.pages]
                resume_text = "\n\n".join(pages).strip()
                if resume_text:
                    st.session_state.resume_text = resume_text
                    st.success("Resume loaded successfully!")
                else:
                    st.error("Could not extract text from the PDF. Try a text-based PDF.")
            except Exception as exc:
                st.error(f"Error reading PDF: {exc}")

    if st.session_state.resume_text:
        st.write("**Resume preview:**")
        st.write(st.session_state.resume_text[:300] + ("..." if len(st.session_state.resume_text) > 300 else ""))

    if st.button("Clear History"):
        st.session_state.history = []
        st.success("History cleared.")

st.header("Ask the Agent")
user_query = st.text_area("Job search query or instructions", height=120)
if st.button("Search Jobs"):
    if not user_query.strip():
        st.warning("Please enter a message for the agent.")
    else:
        with st.spinner("Running the agent... this may take a moment"):
            try:
                response = run_agent(user_query, st.session_state.history, resume_text=st.session_state.resume_text)
                st.success("Agent completed successfully.")
            except Exception as exc:
                st.error(f"Agent error: {exc}")

if st.session_state.history:
    st.markdown("## Conversation History <a id='conversation-history'></a>", unsafe_allow_html=True)
    for item in st.session_state.history:
        if item["role"] == "user":
            st.markdown(f"**You:** {item['content']}")
        else:
            st.markdown(f"**Agent:** {item['content']}")
else:
    st.markdown("## Conversation History <a id='conversation-history'></a>", unsafe_allow_html=True)
    st.info("No conversation history yet. Enter a job query to begin.")

st.markdown("---")
st.caption("Powered by the Job Hunter Agent backend. Upload a PDF resume and ask the agent for job search help.")
