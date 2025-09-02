import os
from dotenv import load_dotenv

load_dotenv()  # load .env file

HF_API_KEY = os.getenv("HF_API_KEY")
DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME")
}


HF_API_URL = "https://api-inference.huggingface.co/models/t5-small"


