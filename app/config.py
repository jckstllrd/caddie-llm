import os

from dotenv import load_dotenv

load_dotenv()


FOREGONE_FRONTEND_URL = str(os.getenv("FOREGONE_FRONTEND_URL"))
API_KEY = os.getenv("OPENAI_API_KEY")
ORGANISATION_KEY = os.getenv("OPENAI_ORGANISATION_ID")
