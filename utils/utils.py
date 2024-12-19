from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import requests
from bs4 import BeautifulSoup
import re

AOC_TZ = ZoneInfo("US/Eastern")

def AOC_now():
    ''' Return datetime.now in US/Eastern, which is the timezone AOC uses'''
    return datetime.now().astimezone(AOC_TZ)


def read_file_to_string(filename):
    ''' Reads a file to a string '''
    with open(filename, "r") as f:
        return f.read()


def write_string_to_file(filename, string):
    ''' Writes a string to a text file, will also create parent folders if they don't exist '''
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(string)


def download_file(url, filename, skip_if_exists=True, **kwargs) -> str:
    ''' Downloads a url to a file'''
    path = Path(filename)
    if skip_if_exists and path.exists():
        return read_file_to_string(path)
    text = requests.get(url, **kwargs).text
    write_string_to_file(path, text)
    return text


def get_example_input_from_html(html_text):
    """ Extract Example Inputs from AOC Puzzle description HTML File """
    soup = BeautifulSoup(html_text, features="html.parser")
    pres = soup.find_all("pre")
    if len(pres) == 1:
        return pres[0].get_text()
    elif len(pres) > 1:
        return (
            "MULTIPLE PRE TAGS FOUND"
            + "\n\n"
            + "\n\n".join(pre.get_text() for pre in pres)
        )
    else:
        return ""

def extract_test_input(puzzle_html_filename, test_input_filename):
    """ extract test input from puzzle html file and save to a text file. """
    if not test_input_filename.exists():
        example_input = get_example_input_from_html(
            read_file_to_string(puzzle_html_filename)
        )
        if example_input:
            write_string_to_file(test_input_filename, example_input)
        else:
            print(f"Could not find <pre> tag in puzzle HTML file:\n{puzzle_html_filename}")



def parse_puzzle_code(code: str) -> tuple[int, int]:
    # get current date as per US/Eastern, which is what AOC is configured on
    today = AOC_now()
    match re.split(r"[\/\-\.]", code):
        case [""]:
            return today.year, today.day
        case [day]:
            return today.year, int(day)
        case [year, day]:
            return int(year), int(day)
        case something_else:
            raise ValueError(f'Could not parse code "{code}"')