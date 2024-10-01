"""
Terminology:
- API (Application Programming Interface): Used to get live data from external sources (TMDB in this case).
- Variables: These are things that can be changed later, like a movie or genre.
- JSON (JavaScript Object Notation): The format in which the API sends back data.
- PostgreSQL: A database where I can store and retrieve data.
- URL: https://www.themoviedb.org/settings/api
"""

# Movie Night Decision Maker App

# Importing libraries
import requests  # This library is used to send HTTP requests to the API
import psycopg2  # This is used to connect and interact with the PostgreSQL database
from dotenv import load_dotenv  # This helps load environment variables from the .env file
import os  # This allows access to environment variables like API keys and database credentials
import streamlit as st # The st refers to Streamlit. 

# Load data from .env file
load_dotenv()  # Loading everything from the .env file like the API key and token and login details.

# Getting the API key and database logins
api_key = os.getenv("API_KEY")  # The API key I got from the TMDB website
db_username = os.getenv("DB_USERNAME")  # The username for my database
db_password = os.getenv("DB_PASSWORD")  # The password for my database
db_host = os.getenv("DB_HOST")  # The host where my database is stored
db_port = os.getenv("DB_PORT")  # The port to connect to the database
db_name = os.getenv("DB_NAME")  # The name of my database

# Connecting to the PostgreSQL database
def connect_to_db():
    connection = psycopg2.connect(
        host=db_host,         # Host address for the database
        database=db_name,     # Name of the database
        user=db_username,     # Username for the database
        password=db_password  # Password for the database
    )
    return connection

# Function to create the table
def create_table(cur):
    create_table_SQL = """
    CREATE TABLE IF NOT EXISTS student.de10_rm_movies_shows (
        id SERIAL PRIMARY KEY,
        movie_id INTEGER NOT NULL,
        cast TEXT NOT NULL,
        crew TEXT NOT NULL,
        keywords TEXT NOT NULL,
        original_title VARCHAR(255) NOT NULL,
        production_companies TEXT[] NOT NULL,
        production_countries TEXT[] NOT NULL,
        status VARCHAR(50) NOT NULL,
        tagline TEXT NOT NULL,
        title VARCHAR(255) NOT NULL,
        genre_ids TEXT[] NOT NULL,
        release_date DATE,
        overview TEXT NOT NULL,
        vote_average NUMERIC,
        vote_count INTEGER,
        poster_path VARCHAR(255) NOT NULL,
        popularity NUMERIC,
        original_language VARCHAR(100) NOT NULL,
        budget BIGINT,
        revenue BIGINT
    )
    """
    cur.execute(create_table_SQL)

# Function to insert/update data in the table
def upsert_data(conn, cur, data):
    sql = """
    INSERT INTO student.de10_rm_movies_shows 
    (movie_id, title, genre_ids, release_date, overview, vote_average, vote_count, poster_path, popularity, original_language, budget, revenue, cast, crew, keywords, original_title, production_companies, production_countries, status, tagline)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (title) DO UPDATE SET
        genre_ids = EXCLUDED.genre_ids,
        release_date = EXCLUDED.release_date,
        overview = EXCLUDED.overview,
        vote_average = EXCLUDED.vote_average,
        vote_count = EXCLUDED.vote_count,
        poster_path = EXCLUDED.poster_path,
        popularity = EXCLUDED.popularity,
        original_language = EXCLUDED.original_language,
        budget = EXCLUDED.budget,
        revenue = EXCLUDED.revenue,
        cast = EXCLUDED.cast,
        crew = EXCLUDED.crew,
        keywords = EXCLUDED.keywords,
        original_title = EXCLUDED.original_title,
        production_companies = EXCLUDED.production_companies,
        production_countries = EXCLUDED.production_countries,
        status = EXCLUDED.status,
        tagline = EXCLUDED.tagline;
    """

    for item in data['results']:
        cur.execute(sql, (
            item.get('id'),
            item.get('title'),
            item.get('genre_ids', []),
            item.get('release_date'),
            item.get('overview'),
            item.get('vote_average'),
            item.get('vote_count'),
            item.get('poster_path'),
            item.get('popularity'),
            item.get('original_language'),
            item.get('budget', 0),
            item.get('revenue', 0),
            item.get('cast', ''),
            item.get('crew', ''),
            item.get('keywords', ''),
            item.get('original_title'),
            item.get('production_companies', []),
            item.get('production_countries', []),
            item.get('status', ''),
            item.get('tagline', '')
        ))
    conn.commit()

# Function to fetch data from the TMDB API
def fetch_data(api_url, api_token):
    headers = {  # Set up headers for the API request
        "Authorization": f"Bearer {api_token}"  # Use the API token for authorization
    }
    response = requests.get(api_url, headers=headers)  # Send a GET request to the API URL
    return response.json()  # Return API response as JSON

# API endpoint for fetching popular movies
api_url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
api_token = api_key  # API token loaded from the .env file

# Fetch data from TMDB
data = fetch_data(api_url, api_token)

# Check if data was successfully retrieved and insert into the database
if data and 'results' in data:
    db_connection = connect_to_db()  # Establish database connection
    cur = db_connection.cursor()  # Create a cursor
    
    # Call the create_table function to ensure the table exists
    create_table(db_connection, cur)
    
    # Insert/Update data in the database
    upsert_data(db_connection, cur, data)
    
    # Close the cursor and connection after everything is done
    cur.close()  
    db_connection.close()  
    
    print("Data has been added to the database!")  # Success message
else:
    print("No data available at the moment.")  # Error message if no data is available











# Streamlit app title
st.title("Movie Night Decision Maker 🎬")

# Introduction text
st.write("Not sure what to watch? Let us find a movie or show for you!")











