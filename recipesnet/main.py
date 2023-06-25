import logging
import os
from pathlib import Path
import sys

from recipesnet.recipes import load_all_graphs

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s"
)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "make-graphs":
        load_all_graphs()
        return

    os.system(f"streamlit run {Path(__file__).parent}/Home.py")
