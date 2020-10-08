from movie.adapters.repository import instance as repo


def get_number_of_movies():
    return repo.get_number_of_movies()


def get_genres():
    return repo.get_genres()
