from pathlib import Path
import requests
from bs4 import BeautifulSoup

def read_file_to_string(filename):
    with open(filename, 'r') as f:
        return f.read()

def write_string_to_file(filename, string):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(string)

def download_file(url, filename, skip_if_exists = True, **kwargs):
    path = Path(filename)
    if skip_if_exists and path.exists():
        return
    r = requests.get(url, **kwargs)
    write_string_to_file(path, r.text)

def get_example_input_from_html(html_text):
    soup = BeautifulSoup(html_text, features="html.parser")
    pres = soup.find_all('pre')
    if len(pres) == 1:
        return pres[0].get_text()
    elif len(pres) > 1:
        return 'MULTIPLE PRE TAGS FOUND'
    else: 
        return ''