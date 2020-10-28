from typing import List, Set, Union, Dict, OrderedDict
from csv import DictReader

from movie.domain.movie import Movie
from movie.domain.actor import Actor
from movie.domain.genre import Genre
from movie.domain.director import Director


class MovieFileCSVReader:
    _ROW = Union[Dict[str, str], OrderedDict[str, str]]

    _REQUIRED_FIELDS: List[str] = [
        'Rank',
        'Title',
        'Genre',
        'Description',
        'Director',
        'Actors',
        'Year',
        'Runtime (Minutes)',
        'Rating',
        'Votes',
        'Revenue (Millions)',
        'Metascore'
    ]

    def __init__(self, file_name: str):
        self._file_name = file_name
        self._dataset_of_movies: List[Movie] = []
        self._dataset_of_actors: List[Actor] = []
        self._dataset_of_directors: List[Director] = []
        self._dataset_of_genres: List[Genre] = []

        self._actors: Dict[Actor, Actor] = {}
        self._directors: Dict[Director, Director] = {}
        self._genres: Dict[Genre, Genre] = {}

    @property
    def _file_name(self):
        return self.__file_name

    @_file_name.setter
    def _file_name(self, file_name):
        if not isinstance(file_name, str):
            raise TypeError(f"'file_name' must be of type 'str' but was '{type(file_name).__name__}'")

        if not file_name.endswith('.csv'):
            raise ValueError(f"'{file_name}' is not a csv file")

        self.__file_name = file_name

    @property
    def dataset_of_movies(self):
        return self._dataset_of_movies

    @property
    def dataset_of_actors(self):
        return self._dataset_of_actors

    @property
    def dataset_of_directors(self):
        return self._dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self._dataset_of_genres

    def _get_dict_value(self, key, dictionary: Dict):
        try:
            return dictionary[key]
        except KeyError:
            dictionary[key] = key
            return key

    def _get_actor(self, actor: Actor) -> Actor:
        return self._get_dict_value(actor, self._actors)

    def _get_director(self, director: Director) -> Director:
        return self._get_dict_value(director, self._directors)

    def _get_genre(self, genre: Genre) -> Genre:
        return self._get_dict_value(genre, self._genres)

    def _read_row(self, row: _ROW, id_: int) -> Movie:
        """
        Helper method to construct a Movie from a row.

        Raises:
            ValueError: unable to parse row: {row}
         """
        error = False

        try:
            title = row['Title']
            genres = [self._get_genre(Genre(name)) for name in row['Genre'].split(',')]
            description = row['Description']
            director = self._get_director(Director(row['Director']))
            actors = [self._get_actor(Actor(name)) for name in row['Actors'].split(',')]
            release_year = int(row['Year'])
            runtime_minutes = int(row['Runtime (Minutes)'])
            rating = float(row['Rating'])
            votes = int(row['Votes'])
            revenue_millions = float(row['Revenue (Millions)']) if row['Revenue (Millions)'] != 'N/A' else None
            metascore = int(row['Metascore']) if row['Metascore'] != 'N/A' else None
        except KeyError:
            error = True
        except ValueError:
            error = True

        if error:
            raise ValueError(f'unable to parse row: {row}')

        movie = Movie(title, release_year, id_)
        movie.genres = genres
        movie.description = description
        movie.director = director
        movie.actors = actors
        movie.runtime_minutes = runtime_minutes
        movie.rating = rating
        movie.votes = votes

        if revenue_millions:
            movie.revenue_millions = revenue_millions

        if metascore:
            movie.metascore = metascore

        return movie

    def read_csv_file(self, max_num_lines: int = None):
        unique_movies: Set[Movie] = set()
        unique_actors: Set[Actor] = set()
        unique_directors: Set[Director] = set()
        unique_genres: Set[Genre] = set()

        self._actors = {}
        self._directors = {}
        self._genres = {}

        count = 0

        with open(self._file_name, mode='r', encoding='utf-8-sig') as file:
            movie_file_reader = DictReader(file)

            # Check if fields are missing
            for field in self._REQUIRED_FIELDS:
                if field not in movie_file_reader.fieldnames:
                    raise ValueError(f"'{self._file_name}' missing field '{field}'")

            for row in movie_file_reader:

                # Only read up to max_num_lines lines
                if max_num_lines and count >= max_num_lines:
                    break

                try:
                    movie = self._read_row(row, count)
                except ValueError:
                    # Failed to parse row to Movie
                    continue

                count += 1

                unique_movies.add(movie)

                # Add colleagues to each actor
                for actor in movie.actors:
                    unique_actors.add(actor)

                    for colleague in movie.actors:
                        actor.add_actor_colleague(colleague)

                unique_directors.add(movie.director)

                for genre in movie.genres:
                    unique_genres.add(genre)

        self._dataset_of_movies = list(unique_movies)
        self._dataset_of_actors = list(unique_actors)
        self._dataset_of_directors = list(unique_directors)
        self._dataset_of_genres = list(unique_genres)
