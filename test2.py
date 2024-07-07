import requests
import sqlite3

# Replace 'your_api_key' with your actual OMDB API key
API_KEY = '4ebbaf53'
BASE_URL = 'http://www.omdbapi.com/'


class Movie:
    def __init__(self, title, year, plot, imdb_rating):
        self.title = title
        self.year = year
        self.plot = plot
        self.imdb_rating = imdb_rating


class OMDBClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_movie_data(self, title):
        params = {
            't': title,
            'apikey': self.api_key
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['Response'] == 'True':
                return Movie(data['Title'], data['Year'], data['Plot'], data['imdbRating'])
            else:
                print(f"Error: {data['Error']}")
        else:
            print(f"HTTP Error: {response.status_code}")
        return None


class MovieDatabase:
    def __init__(self, db_name='movies.db'):
        self.db_name = db_name
        self._create_database()

    def _create_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                year TEXT,
                plot TEXT,
                imdb_rating TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def insert_movie(self, movie):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO movies (title, year, plot, imdb_rating)
            VALUES (?, ?, ?, ?)
        ''', (movie.title, movie.year, movie.plot, movie.imdb_rating))
        conn.commit()
        conn.close()

    def reset_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS movies')
        conn.commit()
        conn.close()
        self._create_database()

    def fetch_all_movies(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM movies')
        movies = cursor.fetchall()
        conn.close()
        return movies


def main():
    omdb_client = OMDBClient(API_KEY)
    movie_db = MovieDatabase()

    while True:
        title = input("Enter the movie title (or 'exit' to quit): ")
        if title.lower() == 'exit':
            break
        movie = omdb_client.fetch_movie_data(title)
        if movie:
            movie_db.insert_movie(movie)
            print(f"Inserted data for {movie.title}")
        else:
            print(f"Failed to fetch data for {title}")

    # Fetch all movies from the database
    movies = movie_db.fetch_all_movies()
    for movie in movies:
        print(movie)


if __name__ == '__main__':
    # Resetting the database before running the main program
    db = MovieDatabase()
    db.reset_database()
    main()
