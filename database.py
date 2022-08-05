import os
import psycopg2
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
);"""

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
);"""

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched(
    movie_id INTEGER,
    user_username TEXT,
    FOREIGN KEY (user_username) REFERENCES users(username),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (%s, %s);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = %s"
SEARCH_MOVIE = "SELECT * FROM movies WHERE title LIKE %s;"

SELECT_ALL_MOVIES = "SELECT * FROM movies"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"

INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_username, movie_id) VALUES (%s, %s);"
SELECT_WATCHED_MOVIES = """SELECT movies.* FROM movies 
    JOIN watched ON movies.id = watched.movie_id 
    JOIN users ON users.username = watched.user_username 
    WHERE users.username = %s;"""
SET_MOVIE_WATCHED = "INSERT INTO watched (user_username, movie_id) VALUES (%s, %s);"

INSERT_USER = "INSERT INTO users (username) VALUES (%s);"

CREATE_RELEASEDATE_INDEX = "CREATE INDEX IF NOT EXISTS idx_movies_release ON movies(release_timestamp);"
connection = psycopg2.connect(os.environ["DATABASE_URL"])


def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_WATCHED_TABLE)
            cursor.execute(CREATE_RELEASEDATE_INDEX)

def add_movie(title: str, release_timestamp):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIES, (title, release_timestamp))


def search_movie(pattern):
    with connection:
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            cursor.execute(SEARCH_MOVIE, (f"%{pattern}%", ))
            return cursor.fetchall()

def get_movies(upcoming=False):
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                today_timestamp = datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
            else:
                cursor.execute(SELECT_ALL_MOVIES)
            return cursor.fetchall()


def watch_movie(username: str, movie_id: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_WATCHED_MOVIE, (username, movie_id))


def get_watched_movies(username: str):
    with connection:
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            cursor.execute(SELECT_WATCHED_MOVIES, (username, ))
            return cursor.fetchall()


def add_user(username: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username, ))
