"""
Terminology:

- API (Application Programming Interface): Used to get live data from external sources (TMDB in this case).
- Variables: Things you can change later, like a movie or genre.
- JSON (JavaScript Object Notation): The format in which the API sends back data.
- PostgreSQL: A database where I can store and retrieve data.
"""

# Movie Night Decision Maker App

# Importing libraries
import requests
import psycopg2
from dotenv import load_dotenv
import os

# Load data from .env file
load_dotenv()

# Getting the API key and database data
api_key = os.getenv("API_KEY")  # The API key I got from the TMDB website
db_username = os.getenv("DB_USERNAME")  # The username for my database
db_password = os.getenv("DB_PASSWORD")  # The password for my database
db_host = os.getenv("DB_HOST")  # The host where my database is stored
db_port = os.getenv("DB_PORT")  # The port to connect to the database
db_name = os.getenv("DB_NAME")  # The name of my database

# Function to connect to the PostgreSQL database 
def connect_to_db():
    connection = psycopg2.connect(
        host=db_host,
        database=db_name,  
        user=db_username,  
        password=db_password  
    )
    return connection

# Function to insert data into the PostgreSQL database
def insert_data_to_db(connection, data):
    cursor = connection.cursor()
    for item in data['results']:
        ## Insert data into the database
        cursor.execute(
            "INSERT INTO movies_shows (title, genre_ids) VALUES (%s, %s)",
            (item['title'], item['genre_ids'])
        )
    connection.commit()  # Saves changes to the database
    cursor.close()
    connection.close()  # This should close the connection when everything is done

# Function to fetch data from the TMDB API
def fetch_data(api_url, api_token):
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(api_url, headers=headers)
    return response.json()

# TMDB API (using the API Read Access Token)
api_url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
api_token = api_key

# Fetch data from the TMDB API
data = fetch_data(api_url, api_token)

# If data is fetched, connect to the database and insert data:
if data:
    db_connection = connect_to_db()
    insert_data_to_db(db_connection, data)
    print("Data has been added to the database!")
else:
    print("No data available at the moment.")
