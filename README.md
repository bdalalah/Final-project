# python code 

import requests
import sqlite3

API_KEY = '4ebbaf53'
BASE_URL = 'http://www.omdbapi.com/'

    import requests: This imports the requests library, which allows Python to send HTTP requests easily.
    import sqlite3: This imports the sqlite3 library, which provides a lightweight disk-based database that doesn’t require a separate server process.


==> class Movie:
    def __init__(self, title, year, plot, imdb_rating):
        self.title = title
        self.year = year
        self.plot = plot
        self.imdb_rating = imdb_rating

    class Movie: This defines a class Movie which has attributes title, year, plot, and imdb_rating. This class is used to represent movie data fetched from the OMDB API.


==> class OMDBClient:
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

    class OMDBClient: This class interacts with the OMDB API to fetch movie data.
        __init__(self, api_key): Constructor to initialize the class with an OMDB API key.
        fetch_movie_data(self, title): Method to fetch movie data from OMDB based on the provided title. It constructs an API request, sends it using requests.get(), and processes the response. If successful (response.status_code == 200), it creates a Movie object using fetched data. Otherwise, it prints an error message.



==> class MovieDatabase:
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

    class MovieDatabase: This class manages a SQLite database (movies.db) for storing movie information.
        __init__(self, db_name='movies.db'): Constructor that initializes the database name and creates the database structure using _create_database() method.
        _create_database(self): Method to create the movies table if it doesn't exist in the SQLite database.
        insert_movie(self, movie): Method to insert a Movie object into the movies table.
        reset_database(self): Method to drop the movies table and recreate it, effectively resetting the database.
        fetch_all_movies(self): Method to fetch all movies from the movies table and return them as a list of tuples.



==> def main():
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
    db = MovieDatabase()
    db.reset_database()
    main()

    def main(): The main function of the script.
        Creates instances of OMDBClient and MovieDatabase.
        Runs a loop where it prompts the user to enter a movie title or 'exit' to quit.
        Calls omdb_client.fetch_movie_data(title) to fetch movie data from OMDB.
        If successful, it inserts the movie data into the database using movie_db.insert_movie(movie).
        Finally, it fetches and prints all movies from the database using movie_db.fetch_all_movies().

    if __name__ == '__main__':: This conditional block ensures that the main() function is executed when the script is run directly (not when imported as a module).

## In summary, this Python script interacts with the OMDB API to fetch movie data based on user input, stores the fetched data in a SQLite database, and provides functionality to reset the database or fetch all stored movies. It demonstrates basic principles of API interaction, database handling using SQLite, and modular programming.
