from demo.crew import Demo


def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI is booming or it just a ai bubble?',
       
    }

    try:
        Demo().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

