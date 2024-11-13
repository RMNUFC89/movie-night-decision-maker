# Digital Futures Captsone
# Movie Night Decision Maker

## Overview

For my Capstone I have decided to create a Streamlit app to help absolutely everyone decide what sort of movie they'll watch when they're not sure or limited on time. It can also be used for couple’s who can’t land on a selection for a movie night. The app will allow you to filter between time you have available, genres, or whether you want a TV show or Movie which will then tailor this to you.

### Features

• Downtime: Select how much time you have, and the app will recommend content that fits within that time frame.  
• Genre Filter: Choose the genre you are in mood for that night.  
• Platform Filter: The app can filter suggestions based on platform preferences for Netflix, Disney+, and Amazon Prime.  
• "Already Watched" Option: If you've already seen or played something, you can ask for new recommendations with a single click.

### Requirements

• Python 3.x  
• pip (Python Package Manager)  
• streamlit  
• requests  
• pandas  
• psycopg2-binary (for PostgreSQL)  
• JustWatch API  
• numpy  

### Installation

1) Clone this repository:
https://github.com/RMNUFC89/movie-night-decision-maker.git

2) Navigate to the project directory:
movie-night-decision-maker

3) Install the necessary dependencies from requirements.txt:
pip install -r requirements.txt

4) Create a .env file and add your JustWatch API key:
API_KEY = 'your-justwatch-api-key'

5) Run the Streamlit app locally:
streamlit run streamlit_app.py

### License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.
