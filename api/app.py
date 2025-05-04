import uvicorn
import pickle
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import os

app = FastAPI()

base_dir = os.path.dirname(__file__)
movies = pickle.load(open(os.path.join(base_dir, 'movies_list.pkl'), 'rb'))
similarity = pickle.load(open(os.path.join(base_dir, 'similarity.pkl'), 'rb'))

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7e4b636e12f4a8277173702840ec1afb&language=en-US'
    response = requests.get(url)
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        poster_path = data['poster_path']
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"
    
def recommend(movie_name):
    movie_matches = movies[movies['title'].str.lower() == movie_name.lower()]
    if movie_matches.empty:
        return None
    index = movies[movies['title'] == movie_name].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    print(recommend_movie, recommend_poster)
    return recommend_movie, recommend_poster

class MovieRequest(BaseModel):
    movie: str

class MovieResponse(BaseModel):
    movie_list: Dict[str, str]
    movie_poster_link: Dict[str, str]

@app.get("/")
async def home():
    return {"message": "This is a FastAPI application"}

@app.post("/api/movie_list", response_model=MovieResponse)
async def root(request: MovieRequest):
    movie_list, movie_poster = recommend(request.movie.title())
    if not movie_list:
        raise HTTPException(status_code=404, detail="No movie recommendation found")
    
    return {
        "movie_list": {
            'movie_1': movie_list[0],
            'movie_2': movie_list[1],
            'movie_3': movie_list[2],
            'movie_4': movie_list[3],
            'movie_5': movie_list[4]
        },
        "movie_poster_link": {
            'movie_1': movie_poster[0],
            'movie_2': movie_poster[1],
            'movie_3': movie_poster[2],
            'movie_4': movie_poster[3],
            'movie_5': movie_poster[4]
        }
    }

if __name__ == "__main__":
    uvicorn.run(app)