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
# This makes a connection to the PostgreSQL database
def connect_to_db():
    connection = psycopg2.connect(
        host=db_host,         # Host address for the database
        database=db_name,     # Name of the database
        user=db_username,     # Username for the database
        password=db_password  # Password for the database
    )
    return connection

# SQL: Creating the table with additional fields
CREATE TABLE IF NOT EXISTS student.movies_shows (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    genre_ids TEXT[],  -- Store genre IDs as an array
    release_date DATE,
    overview TEXT,
    vote_average NUMERIC,
    vote_count INTEGER,
    poster_path VARCHAR(255),
    popularity NUMERIC,               -- Popularity of the movie
    original_language VARCHAR(10),    -- Language of the movie
    budget BIGINT,                    -- Movie budget
    revenue BIGINT                    -- Movie revenue
);

# Inserting data into the PostgreSQL database
def insert_data_to_db(connection, data):
    cursor = connection.cursor()
    for item in data['results']:
        
        # I found the column names on a project I saw on Kaggle so the below should check to see if each column still exists, if the column isn’t available then it will show None
        if 'title' in item:
            title = item['title']
        else:
            title = None  # Default if 'title' is missing
        
        if 'genre_ids' in item:
            genre_ids = item['genre_ids']
        else:
            genre_ids = []  # Default if 'genre_ids' are missing
        
        if 'release_date' in item:
            release_date = item['release_date']
        else:
            release_date = None  # Default if 'release_date' is missing
        
        if 'overview' in item:
            overview = item['overview']
        else:
            overview = None  # Default if 'overview' is missing
        
        if 'vote_average' in item:
            vote_average = item['vote_average']
        else:
            vote_average = None  # Default if 'vote_average' is missing
        
        if 'vote_count' in item:
            vote_count = item['vote_count']
        else:
            vote_count = None  # Default if 'vote_count' is missing
        
        if 'poster_path' in item:
            poster_path = item['poster_path']
        else:
            poster_path = None  # Default if 'poster_path' is missing
        
        if 'popularity' in item:
            popularity = item['popularity']
        else:
            popularity = None  # Default if 'popularity' is missing
        
        if 'original_language' in item:
            original_language = item['original_language']
        else:
            original_language = None  # Default if 'original_language' is missing
        
        if 'budget' in item:
            budget = item['budget']
        else:
            budget = None  # Default if 'budget' is missing
        
        if 'revenue' in item:
            revenue = item['revenue']
        else:
            revenue = None  # Default if 'revenue' is missing

        # Inserting data into the database
        cursor.execute(
            """
            INSERT INTO student.movies_shows (title, genre_ids, release_date, overview, vote_average, vote_count, poster_path, popularity, original_language, budget, revenue) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,  # SQL query to insert multiple fields
            (
                title,                   # Movie title
                genre_ids,               # Genre IDs
                release_date,            # Movie release date
                overview,                # Movie overview/description
                vote_average,            # Average user rating
                vote_count,              # Total number of votes
                poster_path,             # Poster image path
                popularity,              # Popularity of the movie
                original_language,       # Original language of the movie
                budget,                  # Movie budget
                revenue                  # Movie revenue
            )
        )
    
    connection.commit()  # Commit the changes to save the inserted data
    cursor.close()  # Close the cursor when done and this is needed for using SQL
    connection.close()  # Close the database connection

# Retrieving the data from the TMDB API
# This should get the latest movie data from the TMDB API using the API URL and token in env file
def fetch_data(api_url, api_token):
    headers = {  # Setting up headers for the API request
        "Authorization": f"Bearer {api_token}"  # Using the API token for authorization
    }
    response = requests.get(api_url, headers=headers)  # Sends a GET request to the API URL to retrieve the data from this source
    return response.json()  # Returns the data from the API in JSON format as this is needed for Steamlit

# In this section it should make an endpoint for the API to fetch the data and set up the API token
api_url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"  # The URL to get popular movies
api_token = api_key  # The API token we loaded from the .env file earlier

# Retrieving data from the TMDB API
# This line grabs the data from the API
data = fetch_data(api_url, api_token)

# If data is found, then the below should connect to the database and insert the data
if it is available:
    db_connection = connect_to_db()  # Establish database connection
    insert_data_to_db(db_connection, data)  # Insert data into the database
    print("Data has been added to the database!")  # Success message
else:
    print("No data available at the moment.")  # Error message in case data is unavailable
