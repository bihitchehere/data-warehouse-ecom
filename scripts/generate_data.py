
# Inside scripts/generate_data.py
from config import get_db_config
import psycopg2

# Get the credentials securely
db_params = get_db_config()

# Use them to connect
conn = psycopg2.connect(**db_params)
print("Successfully connected to the database!")