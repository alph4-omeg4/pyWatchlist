import datetime
import database


menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies
4) Watch a movie
5) View watched movies.
6) Add user to the app.
7) Search for a movie.
8) Exit.

Your selection: """
welcome = "Welcome to the watchlist app!"


print(welcome)
database.create_tables()


def prompt_add_movie():
    title = input('Movie title: ')
    release_date = input('Release date (dd-mm-YYYY): ')
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()
    database.add_movie(title, timestamp)


def print_movie_list(heading: str, movies: list):
    print(f"--{heading} movies--")
    for _id, title, release_date in movies:
        movie_date = datetime.datetime.fromtimestamp(release_date)
        human_date = movie_date.strftime('%d %b %Y')
        print(f'{_id}: {title} (on {human_date})')
    print('----\n')


def prompt_watch_movie():
    username = input("Username: ")
    movie_id = input("Enter movieID  you've watched: ")
    print('----\n')
    database.watch_movie(username, movie_id)


def view_all_movies():
    movies = database.get_movies()
    print_movie_list('All', movies)


def view_upcoming_movies():
    movies = database.get_movies(upcoming=True)
    print_movie_list('Upcoming', movies)


def prompt_view_watched_movies():
    username = input("Username: ")
    movies = database.get_watched_movies(username)
    if movies:
        print_movie_list(f"{username}'s watched", movies)
    else:
        print(f"{username} hasn't watch any movies yet!\n")

def prompt_add_user():
    username = input("Username: ")
    database.add_user(username)


def prompt_search_movies():
    pattern = input("Enter partial movie title you look for: ")
    movies = database.search_movie(pattern)
    if movies:
        print_movie_list('Movies found', movies)
    else:
        print("No movies found\n")


while (user_input := input(menu)) != "8":
    if user_input == "1":
        '''Add new movie'''
        prompt_add_movie()
    elif user_input == "2":
        '''View upcoming movies'''
        view_upcoming_movies()
    elif user_input == "3":
        '''View all movies'''
        view_all_movies()
    elif user_input == "4":
        '''Watch a movie'''
        prompt_watch_movie()
    elif user_input == "5":
        '''View watched movies'''
        prompt_view_watched_movies()
    elif user_input == '6':
        '''Reg new user'''
        prompt_add_user()
    elif user_input == '7':
        prompt_search_movies()
    else:
        print("Invalid input, please try again!")
