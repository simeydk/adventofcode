from dataclasses import dataclass
from functools import cached_property, partial
from pathlib import Path
import requests

from utils.env import BASE_URL, SESSION
from utils.utils import download_file, extract_test_input


def submit_answer(year: int, day: int, part:int, answer: int|str):
    url = f"{BASE_URL}/{year}/day/{day}/answer"
    data = {
        'level': part,
        'answer': answer
    }
    print(f"{SESSION=}")
    res = requests.post(url, data, cookies={"session": str(SESSION)})
    return res

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

def get_your_answers(year: int, day: int, part:int, answer: int|str):
    pass
    
Answer = int | str

@dataclass(frozen = True)
class Aoc_Day:
    year: int
    day: int
    BASE_URL: str = BASE_URL
    SESSION: str = SESSION

    @cached_property
    def cookies(self):
        return {"session": self.SESSION}

    @cached_property
    def url(self):
        return f"{self.BASE_URL}/{self.year}/day/{self.day}"

    @cached_property
    def input_url(self):
        return f"{self.url}/input"
    
    @cached_property
    def answer_url(self):
        return f"{self.url}/answer"

    def submit_answer(self, part: int, answer: Answer):
        data = {
        'level': part,
        'answer': answer
        }
        res = requests.post(self.answer_url, data, cookies=self.cookies)
        return res