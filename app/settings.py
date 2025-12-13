import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    EMAIL = os.getenv("EMAIL")
    SECRET = os.getenv("SECRET")
    LLM_API_KEY = os.getenv("AIPIPE_API_KEY")
    LLM_BASE_URL = os.getenv("AIPIPE_BASE_URL", "https://api.aipipe.io/v1")
    MODEL = os.getenv("MODEL_NAME", "openai/gpt-4o-mini")

    HOST = "0.0.0.0"
    PORT = int(os.getenv("PORT", 8000))

    PAGE_TIMEOUT = 30000
    MAX_QUESTION_TIME = 160

settings = Settings()
