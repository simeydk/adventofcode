
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://adventofcode.com"

SESSION: str = os.environ.get("SESSION") or ""
if not SESSION:
        raise ValueError("No Session environment variable found")