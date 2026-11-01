import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

BASE_URL = "https://automationexercise.com"
PASSWORD = os.getenv("TEST_PASSWORD", "VijitAgarwal")
NAME = "Vijit Agarwal"
PHONE = "9999888877"
ADDRESS = "Chanakya University Bangalore"
PIN_CODE = "562001"
CITY = "Bangalore"
COUNTRY = "India"

TEST_ACCOUNTS = {
    "TC01": "Vijit+TC01@chanakya.com",
    "TC02": "Vijit+TC02@chanakya.com",
    "TC03": "Vijit+TC03@chanakya.com",
    "TC04": "Vijit+TC04@chanakya.com",
    "TC05": "Vijit+TC05@chanakya.com",
}
