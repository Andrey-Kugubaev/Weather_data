import os

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent

api_key = os.getenv('API_KEY')
base_url = 'https://api.openweathermap.org/data/2.5/weather'
DATAFILE = BASE_DIR / 'data/list.csv'
db_path = os.getenv('DATABASE_URL')
sentry_dsn = os.getenv('SENTRY_DSN')
si_value = 'metric'
