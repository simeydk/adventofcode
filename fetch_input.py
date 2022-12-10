from datetime import datetime
import os, argparse, re
from functools import partial
from pathlib import Path
from dotenv import load_dotenv
from utils import AOC_TZ, AOC_now, download_file, extract_test_input

load_dotenv()

SESSION = os.environ.get("SESSION")
BASE_URL = "https://adventofcode.com"


def parse_puzzle_code(code: str) -> tuple[int, int]:
    # get current date as per US/Eastern, which is what AOC is configured on
    today = datetime.now(tz=AOC_TZ)
    match re.split(r"[\/\-\.]", code):
        case [""]:
            return today.year, today.day
        case [day]:
            return today.year, int(day)
        case [year, day]:
            return int(year), int(day)
        case something_else:
            raise ValueError(f'Could not parse code "{code}"')


def download_day(year: int, day: int, session: str):
    dl = partial(download_file, cookies={"session": session})

    file_path = Path("./") / str(year) / "data" / f"day{day:02d}"
    url = f"{BASE_URL}/{year}/day/{day}"
    print(url)

    input_filename = file_path / "input.txt"
    puzzle_html_filename = file_path / "puzzle.html"
    test_input_filename = file_path / "test_input.txt"

    input_text = dl(url + "/input", input_filename)
    if input_text.startswith("Please don't repeatedly request") or input_text.startswith("<!DOCTYPE HTML"):
        input_filename.unlink() # Delete the file again
        return
    dl(url, puzzle_html_filename)
    extract_test_input(puzzle_html_filename, test_input_filename)


# today = date.today()
# download_day(today.year, today.day)

if __name__ == "__main__":    
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("puzzle_code", default="")
    parser.add_argument("-s", "--session", default="")
    args = parser.parse_args()
    SESSION = args.session or os.environ.get("SESSION") or ''
    if not SESSION:
        raise ValueError("No Session environment variable found")

    puzzle_code = args.puzzle_code
    year, day = parse_puzzle_code(puzzle_code)
    today = AOC_now()
    if (year, 12, day) > (today.year, today.month, today.day):
        print(f"Error: {year} day {day} is still in the future. It's only {today.strftime('%d %B %Y')} today.")
        quit()
    download_day(year, day, session=SESSION)
