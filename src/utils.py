import json
import random
from datetime import datetime


def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def format_json(data):
    return json.dumps(data, ensure_ascii=False, indent=2)


def normalize_text(value):
    return str(value).strip().lower()


def generate_booking_code():
    today = datetime.now().strftime("%Y%m%d")
    random_number = random.randint(1000, 9999)
    return f"SC-{today}-{random_number}"