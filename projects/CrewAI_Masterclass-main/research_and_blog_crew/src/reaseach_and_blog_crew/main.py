from reaseach_and_blog_crew.crew import ResearchAndBlogCrew


def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI agents in coding'
    }

    try:
        ResearchAndBlogCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


