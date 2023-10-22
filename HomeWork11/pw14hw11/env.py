from dotenv import load_dotenv
import os

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")