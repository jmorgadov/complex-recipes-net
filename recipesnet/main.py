import logging
import os
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s"
)


def main():
    os.system(f"streamlit run {Path(__file__).parent}/Home.py")
