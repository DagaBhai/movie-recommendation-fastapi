import pickle
import requests
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Load pickle files with error handling
base_dir = os.path.dirname(__file__)
try:
    movies_path = os.path.join(base_dir, 'movies_list.pkl')
    similarity_path = os.path.join(base_dir, 'similarity.pkl')
    logger.info(f"Loading movies from {movies_path}")
    movies = pickle.load(open(movies_path, 'rb'))
    logger.info(f"Loading similarity from {similarity_path}")
    similarity = pickle.load(open(similarity_path, 'rb'))
except FileNotFoundError as e:
    logger.error(f"Pickle file not found: {e}")
    raise HTTPException(status_code=500, detail=f"Server error: Missing pickle file - {e}")
except Exception as e:
    logger.error(f"Error loading pickle files: {e}")
    raise HTTPException(status_code=500, detail=f"Server error: {e}")

def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.getenv("TMDB_API_KEY", "7e4b636e12f4a8277173702840ec1afb")}&language=en-US'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        return "https://via.placeholder.com/500x750?text=No+Poster"
    except requests.RequestException as e:
        logger.error(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie_name):
    try:
        movie_matches = movies[movies['title'].str.lower() == movie_name.lower()]
        if movie_matches.empty:
            logger.warning(f"No movie found for name: {movie_name}")
            return None, None
        index = movies[movies['title'].str.lower() == movie_name.lower()].index[0]
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
        recommend_movie = []
        recommend_poster = []
        for i in distance[1:6]:
            movie_id = movies.iloc[i[0]].id
            recommend_movie.append(movies.iloc[i[0]].title)
            recommend_poster.append(fetch_poster(movie_id))
        logger.info(f"Recommendations for {movie_name}: {recommend_movie}")
        return recommend_movie, recommend_poster
    except Exception as e:
        logger.error(f"Error in recommend function for {movie_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {e}")

class MovieRequest(BaseModel):
    movie: str

class MovieResponse(BaseModel):
    movie_list: Dict[str, str]
    movie_poster_link: Dict[str, str]

@app.get("/")
async def home():
    return {"message": "This is a FastAPI application"}

@app.post("/api/movie_list", response_model=MovieResponse)
async def get_movie_recommendations(request: MovieRequest):
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
