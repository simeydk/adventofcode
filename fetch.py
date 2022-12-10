import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import date

from utils import (
    download_file,
    get_example_input_from_html,
    read_file_to_string,
    write_string_to_file,
)

load_dotenv()

SESSION = os.environ.get("SESSION")
BASE_URL = "https://adventofcode.com"


def dl(url, filename):
    download_file(url, filename, cookies={"session": SESSION})


def download_day(year, day):
    file_path = Path("./") / str(year) / "data" / f"day{day:02d}"
    url = f"{BASE_URL}/{year}/day/{day}"
    print(url)
    dl(url + "/input", file_path / "input.txt")
    dl(url, file_path / "puzzle.html")
    if not (file_path / "test_input.txt").exists():
        print(f"make test_input for {day}")
        example_input = get_example_input_from_html(
            read_file_to_string(file_path / "puzzle.html")
        )
        if example_input:
            write_string_to_file(file_path / "test_input.txt", example_input)
        else:
            print(f"Could not find <pre> tag in puzzle HTML for {year} day {day}")


today = date.today()
download_day(today.year, today.day)
