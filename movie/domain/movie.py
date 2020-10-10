from typing import List

from .genre import Genre
from .actor import Actor
from .director import Director


class Movie:
    id_count: int = 0

    def __init__(self, title: str, release_date: int) -> None:
        self._title = title
        self._release_date = release_date
        self._description: str = None
        self._director: Director = None
        self._actors: List[Actor] = None
        self._genres: List[Genre] = None
        self._runtime_minutes: int = None
        self._rating: float = None
        self._votes: int = None
        self._id: int = Movie.id_count
        Movie.id_count += 1

    @property
    def _title(self):
        return self.__title

    @_title.setter
    def _title(self, title: str):
        if title == "" or not isinstance(title, str):
            self.__title = None
        else:
            self.__title = title.strip()

    @property
    def _release_date(self):
        return self.__release_date

    @_release_date.setter
    def _release_date(self, release_date: int):
        if not isinstance(release_date, int):
            raise TypeError(f"'release_date' must be of type 'int' but was '{type(release_date).__name__}'")

        if release_date < 1900:
            raise ValueError("'release_date' must be greater than or equal to 1900")

        self.__release_date = release_date

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title

    @property
    def release_date(self):
        return self._release_date

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
    def genres(self, genres: List[Genre]):
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

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating: float):
        if not isinstance(rating, float):
            raise TypeError(f"'rating' must be of type 'float' but was '{type(rating).__name__}'")

        if rating < 0 or rating > 10:
            raise ValueError("'rating' must be greater than or equal to 0 and less than or equal to 10")

        self._rating = rating

    @property
    def votes(self):
        return self._votes

    @votes.setter
    def votes(self, votes: int):
        if not isinstance(votes, int):
            raise TypeError(f"'votes' must be of type 'int' but was '{type(votes).__name__}'")

        if votes < 0:
            raise ValueError("'votes' must be greater than or equal to 0")

        self._votes = votes

    @property
    def revenue_millions(self):
        return self._revenue_millions

    @revenue_millions.setter
    def revenue_millions(self, revenue_millions: float):
        if not isinstance(revenue_millions, float):
            raise TypeError(f"'revenue_millions' must be of type 'float' but was '{type(revenue_millions).__name__}'")

        if revenue_millions < 0:
            raise ValueError("'revenue_millions' must be greater than or equal to 0")

        self._revenue_millions = revenue_millions

    @property
    def metascore(self):
        return self._metascore

    @metascore.setter
    def metascore(self, metascore: int):
        if not isinstance(metascore, int):
            raise TypeError(f"'metascore' must be of type 'int' but was '{type(metascore).__name__}'")

        if metascore < 0 or metascore > 100:
            raise ValueError("'metascore' must be greater than or equal to 0 and less than or equal to 100")

        self._metascore = metascore

    @property
    def id(self):
        return self._id

    def __repr__(self) -> str:
        return f'<{type(self).__name__} {self._title}, {self._release_date}>'

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
            raise TypeError(f"'genre' must be of type 'Genre' but was '{type(genre).__name__}'")

        if self._genres is None:
            self._genres = []
        elif genre in self._genres:
            return

        self._genres.append(genre)

    def remove_genre(self, genre: Genre) -> None:
        """ Removes the given Genre from this movie. Does nothing if the given Genre isn't in this movie. """
        if not isinstance(genre, Genre):
            raise TypeError(f"'genre' must be of type 'Genre' but was '{type(genre).__name__}'")

        if self._genres is None or genre not in self._genres:
            return

        self._genres.remove(genre)
