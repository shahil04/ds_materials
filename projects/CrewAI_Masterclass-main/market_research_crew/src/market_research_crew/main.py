import warnings
from market_research_crew.crew import MarketResearchCrew
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")



def run():
    """
    Run the crew.
    """
    inputs = {
        "product_idea": "An AI powered tool that take AI Interviews and give feedback on how to improve the answer. The tool will be used by job seekers to prepare for their interviews and by companies to train their employees for interviews."

        # "product_idea": "An AI powered tool that summarizes youtube videos on my channel and posts the summary on various social media platforms like LinkedIn, Instagram, Facebook,X, WhatsApp"
    }

    try:
        MarketResearchCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

