"""Streamlit frontend for MarketResearchCrew."""

from __future__ import annotations
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv, dotenv_values
import os

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT / "src"))

from market_research_crew.crew import MarketResearchCrew

REPORT_PATH = ROOT / "reports" / "report.md"
ENV_PATH = ROOT / ".env"
DEFAULT_PRODUCT_IDEA = (
    "An AI powered tool that takes AI interviews and gives feedback on how to improve answers. "
    "The tool will be used by job seekers to prepare for interviews and by companies to train their employees."
)


def load_env_vars() -> dict:
    """Load current environment variables from .env file."""
    if ENV_PATH.exists():
        return dotenv_values(ENV_PATH)
    return {}


def save_env_var(key: str, value: str) -> None:
    """Save or update an environment variable in .env file."""
    env_vars = load_env_vars()
    env_vars[key] = value
    
    with open(ENV_PATH, "w") as f:
        for k, v in env_vars.items():
            f.write(f"{k}={v}\n")
    
    os.environ[key] = value


def run_crew_page() -> None:
    """Main page for running the crew."""
    st.title("MarketResearchCrew Runner")
    st.write(
        "Use this app to run the MarketResearchCrew on a product idea and review the generated market research report."
    )

    with st.expander("About this frontend", expanded=False):
        st.write(
            "This Streamlit app launches the crew defined in `src/market_research_crew/crew.py`. "
            "It sends a product idea prompt as input and displays the generated report from `reports/report.md`."
        )

    product_idea = st.text_area("Product idea prompt", value=DEFAULT_PRODUCT_IDEA, height=220)
    run_button = st.button("Run MarketResearchCrew", type="primary")

    if run_button:
        if not product_idea.strip():
            st.error("Please enter a product idea before running the crew.")
            return

        st.info("Running crew. This may take a few minutes depending on your agent configuration.")

        try:
            with st.spinner("Launching crew and executing tasks..."):
                MarketResearchCrew().crew().kickoff(inputs={"product_idea": product_idea})
            st.success("Crew execution completed.")
        except Exception as error:
            st.error(f"Crew execution failed: {error}")
            return

        if REPORT_PATH.exists():
            st.subheader("Generated Report")
            report_text = REPORT_PATH.read_text(encoding="utf-8")
            st.code(report_text, language="markdown")
            st.write(f"Report saved to `{REPORT_PATH}`.")
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Download Report as MD",
                    data=report_text,
                    file_name="market_research_report.md",
                    mime="text/markdown",
                )
            with col2:
                st.download_button(
                    label="📥 Download Report as TXT",
                    data=report_text,
                    file_name="market_research_report.txt",
                    mime="text/plain",
                )
        else:
            st.warning(
                "Crew finished, but no report was found at `reports/report.md`. "
                "Check your crew task configuration and output file settings."
            )


def settings_page() -> None:
    """Settings page for environment configuration."""
    st.title("⚙️ Configuration Settings")
    st.write("Configure your API keys and model settings for the .env file.")
    
    env_vars = load_env_vars()
    
    st.subheader("OpenAI Configuration")
    
    api_key = st.text_input(
        "OpenAI API Key",
        value=env_vars.get("OPENAI_API_KEY", ""),
        type="password",
        help="Your OpenAI API key for authentication."
    )
    
    model_name = st.text_input(
        "Model Name",
        value=env_vars.get("MODEL_NAME", "gpt-4"),
        help="The model to use (e.g., gpt-4, gpt-3.5-turbo)."
    )
    
    st.subheader("Additional API Keys (Optional)")
    
    serper_api_key = st.text_input(
        "Serper API Key (for web search)",
        value=env_vars.get("SERPER_API_KEY", ""),
        type="password",
        help="API key for Serper web search tool."
    )
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save Configuration", type="primary", use_container_width=True):
            if not api_key.strip():
                st.error("OpenAI API Key is required.")
                return
            
            try:
                save_env_var("OPENAI_API_KEY", api_key)
                save_env_var("MODEL_NAME", model_name)
                if serper_api_key.strip():
                    save_env_var("SERPER_API_KEY", serper_api_key)
                
                st.success("✅ Configuration saved to `.env` file!")
                st.info("The settings will take effect on the next crew run.")
            except Exception as e:
                st.error(f"Failed to save configuration: {e}")
    
    with col2:
        if st.button("🔄 Reload from .env", use_container_width=True):
            st.rerun()
    
    st.subheader("Current .env Content")
    if ENV_PATH.exists():
        env_content = ENV_PATH.read_text(encoding="utf-8")
        st.code(env_content, language="bash")
    else:
        st.info("No `.env` file found yet. Create one by saving configuration above.")


def main() -> None:
    """Main app with sidebar navigation."""
    st.set_page_config(page_title="MarketResearchCrew", page_icon="🤖", layout="wide")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page",
        options=["Run Crew", "Settings"]
    )
    
    st.sidebar.divider()
    st.sidebar.info(
        "📚 **Quick Links**\n"
        "- [crewAI Docs](https://docs.crewai.com)\n"
        "- [Streamlit Docs](https://docs.streamlit.io)"
    )
    
    if page == "Run Crew":
        run_crew_page()
    elif page == "Settings":
        settings_page()


if __name__ == "__main__":
    main()
