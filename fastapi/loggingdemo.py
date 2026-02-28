import logging

# Configure logging to save to a file named 'app.log'
# filemode='a' appends new logs (default); use 'w' to overwrite the file on each run
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

logging.info("A user logged in successfully.")
logging.warning("Disk space is low.")
logging.error("An unexpected error occurred.")


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("Saved to file")
