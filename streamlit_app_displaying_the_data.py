# streamlit_app.py

import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to the PostgreSQL database
def connect_to_db():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

# Function to retrieve data from the database
def get_data():
    conn = connect_to_db()
    cur = conn.cursor()
    
    # Fetch the movies/shows data
    cur.execute("SELECT title, genre_ids, release_date, overview, vote_average, vote_count, runtime, streaming_app FROM student.de10_rm_movies_shows;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

# Streamlit app interface
st.title("Movie Night Decision Maker 🎬")

# Introduction text
st.write("Not sure what to watch? Let us find a movie or show for you!")

# Retrieve data
data = get_data()

# 1. Select Streaming App (Dropdown)
streaming_apps = ["Netflix", "Amazon Prime", "Disney+", "Hulu", "HBO Max"]  # Example streaming apps
selected_app = st.selectbox("Choose your preferred streaming app:", streaming_apps)

# 2. Set Available Time (Slider)
max_runtime = st.slider("Select how much time you have (in minutes):", min_value=30, max_value=240, step=10)
hours = max_runtime // 60
minutes = max_runtime % 60

# Display time in hours and minutes
st.write(f"You have {hours} hours and {minutes} minutes available to watch something.")

# 3. Select Genre (Multiple Select)
genres = ["Action", "Comedy", "Drama", "Fantasy", "Horror", "Romance", "Thriller", "Sci-Fi", "Documentary"]  # Example genres
selected_genres = st.multiselect("Pick your favorite genres:", genres)

# 4. Movie or TV Show Selection
content_type = st.radio("What are you in the mood for?", ("Movie", "TV Show"))

# Filter the data based on user choices
filtered_data = []
for item in data:
    title, genre_ids, release_date, overview, vote_average, vote_count, runtime, streaming_app = item

    # Filter by selected streaming app
    if streaming_app == selected_app:

        # Filter by selected genres (if any)
        if not selected_genres or any(genre in genre_ids for genre in selected_genres):

            # Filter by runtime
            if runtime <= max_runtime:

                # Filter by content type
                if content_type == "Movie" and "movie" in overview.lower():
                    filtered_data.append(item)
                elif content_type == "TV Show" and "tv show" in overview.lower():
                    filtered_data.append(item)

# Show results
if filtered_data:
    st.write(f"Here are some suggestions for you:")
    for item in filtered_data:
        title, genre_ids, release_date, overview, vote_average, vote_count, runtime, streaming_app = item
        st.write(f"**{title}**")
        st.write(f"Genres: {', '.join(genre_ids)}")
        st.write(f"Release Date: {release_date}")
        st.write(f"Runtime: {runtime} minutes")
        st.write(f"Average Rating: {vote_average} based on {vote_count} votes")
        st.write("---")
else:
    st.write("No suggestions found based on your preferences. Try adjusting your filters.")
