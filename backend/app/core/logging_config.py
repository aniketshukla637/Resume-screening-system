"""
Centralized logging setup. Import `setup_logging()` once in main.py.
"""
import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("error.log", encoding="utf-8"),
        ],
    )
    logging.getLogger("multipart").setLevel(logging.WARNING)