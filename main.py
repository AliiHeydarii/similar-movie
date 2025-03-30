from fastapi import FastAPI, Query, HTTPException
from dotenv import load_dotenv
import requests
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')

app = FastAPI()

@app.get('/similar-movies/')
def get_similar_movies(movie_name:str = Query(..., description='movie name')):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API KEY MISSING")
    
    url = f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}&language=fa'
    response = requests.get(url)
    data = response.json()
    movie_id = data['results'][0]['id']

    similar_movies_url = f'https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={API_KEY}&language=fa'
    similar_movies_response = requests.get(similar_movies_url)

    if similar_movies_response.status_code != 200:
        raise HTTPException(status_code=similar_movies_response.status_code, detail='can not find similar movies')


    similar_movies = similar_movies_response.json()


    movies_data = []
    for movie in similar_movies['results']:
        movies_data.append({
            "title" : movie.get("title"),
            "overview" : movie.get("overview"),
            "release_date" : movie.get("release_date"),
            "vote_average" : movie.get("vote_average")
        })


    return movies_data