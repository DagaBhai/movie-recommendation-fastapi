# 🎬 Movie Recommendation API

A fast and efficient FastAPI application that provides movie recommendations based on a pre-trained similarity model, complete with movie titles and poster links fetched from The Movie Database (TMDb) API. Perfect for movie enthusiasts or developers looking to integrate a recommendation system into their projects!

---

## 🚀 Features

- **Movie Recommendations**: Get 5 movie recommendations based on a provided movie title using a precomputed similarity matrix.
- **Poster Fetching**: Retrieves movie poster URLs from TMDb for a visually appealing response.
- **FastAPI Backend**: Lightweight and high-performance API built with FastAPI for quick responses.
- **Error Handling**: Robust handling for cases where movies are not found or API requests fail.
- **Structured Responses**: Returns JSON with movie titles and poster links in a clean, organized format.
- **Pre-trained Model**: Uses pickled data (`movies_list.pkl` and `similarity.pkl`) for fast recommendation generation.

---

## 🛠️ Prerequisites

To run this application, ensure you have the following:

- **Python 3.8+**
- **TMDb API Key**: Obtain an API key from [The Movie Database (TMDb)](https://www.themoviedb.org/).
- **Dependencies** (install via `requirements.txt`):
  - `fastapi`
  - `uvicorn`
  - `requests`
  - `pydantic`
  - `pandas` (for handling the movie dataset)
  - `pickle` (for loading pre-trained models)

Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## 📂 Project Structure

```
project_directory/
│
├── app.py                   # Main FastAPI application
├── movies_list.pkl          # Pickled file containing the movie dataset
├── similarity.pkl           # Pickled file containing the similarity matrix
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## ⚙️ Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up TMDb API Key**:
   Update `app.py` with your TMDb API key in the `fetch_poster` function:
   ```python
   url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=<YOUR_TMDB_API_KEY>&language=en-US'
   ```

3. **Prepare Data Files**:
   Ensure `movies_list.pkl` and `similarity.pkl` are in the project directory. These files contain the movie dataset and precomputed similarity matrix, respectively.

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```
   Alternatively, use Uvicorn directly:
   ```bash
   uvicorn app:app --reload
   ```

6. **Access the API**:
   Open your browser or API client (e.g., Postman) and navigate to `http://localhost:8000`.

---

## 🌟 Usage

1. **API Endpoints**:
   - **GET /**: Returns a welcome message to confirm the API is running.
     - Example: `http://localhost:8000/`
     - Response: `{"message": "This is a FastAPI application"}`

   - **POST /api/movie_list**: Accepts a movie title and returns 5 recommended movies with their poster links.
     - Request Body (JSON):
       ```json
       {"movie": "Inception"}
       ```
     - Example Response:
       ```json
       {
         "movie_list": {
           "movie_1": "The Dark Knight",
           "movie_2": "Interstellar",
           "movie_3": "Memento",
           "movie_4": "The Prestige",
           "movie_5": "Shutter Island"
         },
         "movie_poster_link": {
           "movie_1": "https://image.tmdb.org/t/p/w500/abc123.jpg",
           "movie_2": "https://image.tmdb.org/t/p/w500/xyz789.jpg",
           "movie_3": "https://image.tmdb.org/t/p/w500/def456.jpg",
           "movie_4": "https://image.tmdb.org/t/p/w500/ghi789.jpg",
           "movie_5": "https://image.tmdb.org/t/p/w500/jkl012.jpg"
         }
       }
       ```

2. **Testing with cURL**:
   ```bash
   curl -X POST "http://localhost:8000/api/movie_list" -H "Content-Type: application/json" -d '{"movie": "Inception"}'
   ```

3. **Testing with Python**:
   ```python
   import requests

   response = requests.post("http://localhost:8000/api/movie_list", json={"movie": "Inception"})
   print(response.json())
   ```

4. **Interactive API Docs**:
   Visit `http://localhost:8000/docs` for Swagger UI to test the API interactively.

---

## 🎨 Example Interaction

**Request**:
```json
POST /api/movie_list
{"movie": "Inception"}
```

**Response**:
```json
{
  "movie_list": {
    "movie_1": "The Dark Knight",
    "movie_2": "Interstellar",
    "movie_3": "Memento",
    "movie_4": "The Prestige",
    "movie_5": "Shutter Island"
  },
  "movie_poster_link": {
    "movie_1": "https://image.tmdb.org/t/p/w500/abc123.jpg",
    "movie_2": "https://image.tmdb.org/t/p/w500/xyz789.jpg",
    "movie_3": "https://image.tmdb.org/t/p/w500/def456.jpg",
    "movie_4": "https://image.tmdb.org/t/p/w500/ghi789.jpg",
    "movie_5": "https://image.tmdb.org/t/p/w500/jkl012.jpg"
  }
}
```

---

## 🔧 Customization

- **Change Recommendation Logic**: Modify the `recommend` function to adjust the number of recommendations or similarity criteria.
- **Update Data Files**: Regenerate `movies_list.pkl` and `similarity.pkl` with a new dataset or similarity algorithm.
- **Enhance Poster Fetching**: Add fallback mechanisms or support for additional image sizes from TMDb.
- **Add Authentication**: Integrate API key authentication for secure access.

---

## 🐛 Troubleshooting

- **Movie Not Found**: Ensure the movie title matches exactly (case-insensitive) with the dataset in `movies_list.pkl`.
- **TMDb API Errors**: Verify your TMDb API key and internet connection. Check rate limits on the TMDb API.
- **Pickle File Issues**: Ensure `movies_list.pkl` and `similarity.pkl` are present and not corrupted.
- **Server Errors**: Check the console logs for detailed error messages and verify FastAPI/Uvicorn installation.

For further assistance, refer to the [FastAPI Documentation](https://fastapi.tiangolo.com/) or [TMDb API Documentation](https://developers.themoviedb.org/3).

---

## 🌍 Future Enhancements

- Add support for genre-based filtering or user preferences.
- Implement caching for TMDb API requests to reduce latency.
- Add a frontend interface (e.g., Streamlit or React) for user-friendly interaction.
- Support batch recommendations for multiple movie titles.
- Integrate a database for dynamic movie data updates.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙌 Contributing

Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.
