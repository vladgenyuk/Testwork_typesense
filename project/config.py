import os

from dotenv import load_dotenv


load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

TYPESENSE_HOST = os.environ.get("TYPESENSE_HOST")
TYPESENSE_PORT = os.environ.get("TYPESENSE_PORT")
TYPESENSE_PROTOCOL = os.environ.get("TYPESENSE_PROTOCOL")
TYPESENSE_API_KEY = os.environ.get("TYPESENSE_API_KEY")
TYPESENSE_CONNECTION_TIMEOUT_SECONDS = 5
