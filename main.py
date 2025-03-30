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

    return movie_id