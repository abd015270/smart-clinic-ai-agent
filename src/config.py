from pathlib import Path
from dotenv import load_dotenv
import os


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
SKILLS_DIR = BASE_DIR / "skills"

CLINICS_FILE = DATA_DIR / "clinics.json"
DOCTORS_FILE = DATA_DIR / "doctors.json"
DATABASE_FILE = DATA_DIR / "appointments.db"

load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")