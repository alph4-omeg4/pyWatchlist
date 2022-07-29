import sqlite3
from datetime import datetime


CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id INTEGER,
    title TEXT,
    release_timestamp REAL,
    PRIMARY KEY (id)
);"""

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    PRIMARY KEY (username)
);"""

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched(
    movie_id INTEGER,
    user_username TEXT,
    FOREIGN KEY (user_username) REFERENCES users(username),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (?, ?);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = ?"
SEARCH_MOVIE = "SELECT * FROM movies WHERE title LIKE ?;"

SELECT_ALL_MOVIES = "SELECT * FROM movies"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"

INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_username, movie_id) VALUES (?, ?);"
SELECT_WATCHED_MOVIES = """SELECT movies.* FROM movies 
    JOIN watched ON movies.id = watched.movie_id 
    JOIN users ON users.username = watched.user_username 
    WHERE users.username = ?;"""
SET_MOVIE_WATCHED = "INSERT INTO watched (user_username, movie_id) VALUES (?, ?);"

INSERT_USER = "INSERT INTO users (username) VALUES (?);"

CREATE_RELEASEDATE_INDEX = "CREATE INDEX IF NOT EXISTS idx_movies_release ON movies(release_timestamp);"
connection = sqlite3.connect("data.db")


def create_tables():
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_USERS_TABLE)
        connection.execute(CREATE_WATCHED_TABLE)
        connection.execute(CREATE_RELEASEDATE_INDEX)

def add_movie(title: str, release_timestamp):
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))


def search_movie(pattern):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SEARCH_MOVIE, (f"%{pattern}%", ))
        return cursor.fetchall()

def get_movies(upcoming=False):
    with connection:
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_MOVIES)
        return cursor.fetchall()


def watch_movie(username: str, movie_id: str):
    with connection:
        connection.execute(INSERT_WATCHED_MOVIE, (username, movie_id))


def get_watched_movies(username: str):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES, (username, ))
        return cursor.fetchall()


def add_user(username: str):
    with connection:
        connection.execute(INSERT_USER, (username, ))
