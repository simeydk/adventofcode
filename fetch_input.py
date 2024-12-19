from datetime import datetime
import os, argparse, re
from functools import partial
from pathlib import Path
from dotenv import load_dotenv
import requests
from utils.api import download_day
from utils.utils import AOC_TZ, AOC_now, download_file, extract_test_input, parse_puzzle_code

load_dotenv()

if __name__ == "__main__":    
    load_dotenv()
    SESSION = os.environ.get('SESSION')
    parser = argparse.ArgumentParser()
    parser.add_argument("puzzle_code",nargs='?', default="")
    # parser.add_argument("-s", "--session", default="")
    args = parser.parse_args()
    # SESSION = args.session or os.environ.get("SESSION") or ''
    # if not SESSION:
    #     raise ValueError("No Session environment variable found")

    puzzle_code = args.puzzle_code
    year, day = parse_puzzle_code(puzzle_code)
    today = AOC_now()
    if (year, 12, day) > (today.year, today.month, today.day):
        print(f"Error: {year} day {day} is still in the future. It's only {today.strftime('%d %B %Y')} today.")
        quit()
    download_day(year, day, session=SESSION)
