from typing import List

from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director


class Movie:
    def __init__(self, title: str, release_date: int) -> None:
        self.title = title
        self.release_date = release_date
        self._description: str = None
        self._director: Director = None
        self._actors: List[Actor] = None
        self._genres: List[Genre] = None
        self._runtime_minutes: int = None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        if title == "" or not isinstance(title, str):
            self._title = None
        else:
            self._title = title.strip()

    @property
    def release_date(self):
        return self._release_date

    @release_date.setter
    def release_date(self, release_date: int):
        if not isinstance(release_date, int):
            raise TypeError(f"'release_date' must be of type 'int' but was '{type(release_date).__name__}'")

        if release_date < 1900:
            raise ValueError("'release_date' must be greater than or equal to 1900")

        self._release_date = release_date

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: str):
        if description == "" or not isinstance(description, str):
            self._description = None
        else:
            self._description = description.strip()

    @property
    def director(self):
        return self._director

    @director.setter
    def director(self, director: Director):
        if not isinstance(director, Director):
            raise TypeError(f"'director' must be of type 'Director' but was '{type(director).__name__}'")
        self._director = director

    @property
    def actors(self):
        return self._actors

    @actors.setter
    def actors(self, actors: List[Actor]):
        if not isinstance(actors, list):
            raise TypeError(f"'actors' must be of type 'List[Actor]' but was '{type(actors).__name__}'")

        if any(not isinstance(elem, Actor) for elem in actors):
            raise TypeError(f"'actors' must be of type 'List[Actor]' but was '{type(actors).__name__}'")

        if not isinstance(actors, list) and any(not isinstance(elem, Actor) for elem in actors):
            self._actors = []

        self._actors = actors

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, genres: List[Actor]):
        if not isinstance(genres, list):
            raise TypeError(f"'genres' must be of type 'List[Genre]' but was '{type(genres).__name__}'")

        if any(not isinstance(elem, Genre) for elem in genres):
            raise TypeError(f"'genres' must be of type 'List[Genre]' but was '{type(genres).__name__}'")

        self._genres = genres

    @property
    def runtime_minutes(self):
        return self._runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes: int):
        if not isinstance(runtime_minutes, int):
            raise TypeError(f"'runtime_minutes' must be of type 'int' but was '{type(runtime_minutes).__name__}'")

        if runtime_minutes < 1:
            raise ValueError("'runtime_minutes' must be greater than or equal to 1")

        self._runtime_minutes = runtime_minutes

    def __repr__(self) -> str:
        return f'<Movie {self._title}, {self._release_date}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Movie):
            return False
        return self._title == other._title and self._release_date == other._release_date

    def __lt__(self, other) -> bool:
        if not isinstance(other, Movie):
            raise TypeError(
                f"'<' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return f'{self._title}{self._release_date}' < f'{other._title}{other._release_date}'

    def __hash__(self) -> int:
        return hash(f'{self._title}{self._release_date}')

    def add_actor(self, actor: Actor) -> None:
        """ Adds the given Actor to this movie. """
        if not isinstance(actor, Actor):
            raise TypeError(f"'actor' must be of type 'Actor' but was '{type(actor).__name__}'")

        if self._actors is None:
            self._actors = []
        elif actor in self._actors:
            return

        self._actors.append(actor)

    def remove_actor(self, actor: Actor) -> None:
        """ Removes the given Actor from this movie. Does nothing if the given actor isn't in this movie. """
        if not isinstance(actor, Actor):
            raise TypeError(f"'actor' must be of type 'Actor' but was '{type(actor).__name__}'")

        if self._actors is None or actor not in self._actors:
            return

        self._actors.remove(actor)

    def add_genre(self, genre: Genre) -> None:
        """ Adds the given Genre to this movie. """
        if not isinstance(genre, Genre):
            raise TypeError(f"'genre' must be of type 'Actor' but was '{type(genre).__name__}'")

        if self._genres is None:
            self._genres = []
        elif genre in self._genres:
            return

        self._genres.append(genre)

    def remove_genre(self, genre: Genre) -> None:
        """ Removes the given Genre from this movie. Does nothing if the given Genre isn't in this movie. """
        if not isinstance(genre, Genre):
            raise TypeError(f"'genre' must be of type 'Actor' but was '{type(genre).__name__}'")

        if self._genres is None or genre not in self._genres:
            return

        self._genres.remove(genre)
