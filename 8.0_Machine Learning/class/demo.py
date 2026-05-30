# import pandas as pd
# import streamlit as st
# from numpy.random import default_rng as rng

# df = pd.DataFrame(rng(0).standard_normal((20, 3)), columns=["a", "b", "c"])

# st.scatter_chart(df)
def hello_world():
    print("Hello, World!")

import logging

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,  # Log all messages from DEBUG and above
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w' # Overwrite the log file each time the program runs
)

logging.debug("This is a debug message (goes to file).")
logging.info("This is an info message (goes to file).")
logging.warning("This is a warning message (goes to file).")
logging.error("This is an error message (goes to file).")

# Also logs the exception traceback to the file
try:
    1 / 0
except ZeroDivisionError:
    logging.exception("A ZeroDivisionError occurred")
