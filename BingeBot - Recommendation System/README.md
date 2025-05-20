# BingeBot - Movie Recommendation System

### Introduction
BingeBot is a content-based movie recommendation system that helps users discover movies similar to the ones they already like. Built using Python, Streamlit, and the TMDB (The Movie Database) API, this project showcases how machine learning techniques like cosine similarity can be used to build real-world recommendation engines.

Whether you're a movie lover or a data science enthusiast, this project demonstrates how to turn raw movie metadata into a smart, functional product.

### What This Project Does
This application:

- Takes a movie as input from the user.
- Recommends 10 movies that are most similar to it.
- Shows posters of the recommended movies by fetching them from TMDB.
- Uses a content-based filtering approach (based on movie features like genre, cast, etc.).

## Why It Works
This project uses cosine similarity to measure how close two movies are based on their textual features (like genre, director, etc.). Movies with more common characteristics will have higher similarity scores.

The algorithm works on the idea that "similar movies share similar metadata."

## Why This Project Is Useful
- Solves a real-world problem: People often struggle to find good movies to watch. This tool gives instant recommendations.
- Educational: It helps you learn the basics of recommendation systems, cosine similarity, and API integration.
- Practical experience: It shows how to use a machine learning algorithm in a real-life app with a front-end interface.
- Portfolio-worthy: This is a strong addition to your GitHub or resume as it includes ML logic, API use, and UI via Streamlit.

## How It Works – Step by Step
Step 1: Data Preparation (Done in the notebook)
- Movie metadata is collected and cleaned.
- Important features like title, genre, cast, and director are combined into a single text field.
- This combined text is converted into vectors using TF-IDF or CountVectorizer.
- Cosine similarity is calculated between all movie vectors.
- The final result — a similarity matrix and movie DataFrame — is saved in a pickle file (movie_data.pkl).

Step 2: UI and Logic (In the Streamlit app)
- The user opens the Streamlit app and selects a movie from the dropdown.
- When the "Recommend" button is clicked, the app:
- Finds the index of the selected movie.
- Uses the similarity matrix to find the 10 most similar movies.
- Extracts movie titles and TMDB IDs from the dataset.
- Calls the TMDB API to fetch posters for each recommended movie.
- Displays them in a clean 2-row grid format.

## Project Files
Here’s what each file in this project does:

- Recommendation_system.ipynb: Preprocesses the data and builds the recommendation model.
- movie_data.pkl: Pickle file containing the movie DataFrame and similarity matrix.
- app.py: Streamlit app that provides the user interface and connects everything.
- README.txt: You’re reading it!
- requirements.txt: List of Python packages required to run this project.

## How To Use It (Installation + Setup)
### Step 1: Clone the repository
```
Visit the GitHub repo here:
https://github.com/Adityamaurya05/Data-Science-Projects/tree/main/BingeBot%20-%20Recommendation%20System
```
Then clone it:
```
git clone https://github.com/Adityamaurya05/Data-Science-Projects.git
cd Data-Science-Projects/BingeBot - Recommendation System
```
### Step 2: Install dependencies
- If you're using a virtual environment (recommended): 
```
python -m venv venv
venv\Scripts\activate   # For Windows
```
Then install the required packages:
```
pip install -r requirements.txt
```

### Step 3: Get your TMDB API Key
- Go to TMDB and create an account.

- Navigate to API and generate a free key.

- Replace the API key inside app.py in this line:
```
api_key = 'YOUR_TMDB_API_KEY'
```
### Step 4: Run the Streamlit app
Use this command to start the app:
```
streamlit run app.py
```
Your browser will open with the interface. Select a movie and get your recommendations instantly!

### Example Output
The app shows 10 recommended movies with their posters in a neat 2-row format. If any poster is missing, it displays a placeholder image so the layout stays intact.

### Limitations and Future Improvements
- Currently uses only content-based filtering. Could be improved using hybrid or collaborative filtering.
- Poster fetch relies on TMDB — a rate limit or missing ID can cause missing posters.
- Could be enhanced with genre filters, year filters, and user rating integration.

### Skills & Concepts Used
- Python
- Pandas and NumPy
- Machine Learning (cosine similarity)
- Pickle for model storage.
- API usage (TMDB)
- Streamlit for interactive UI
- Data cleaning and preprocessing
- Credits & Acknowledgements
- TMDB for the poster API
- Streamlit for the frontend framework
- Python & open-source community

## Credits & Acknowledgements
- TMDB for the poster API
- Streamlit for the frontend framework
- Python & open-source community

