from typing import List, Set
import csv

from domainmodel.movie import Movie
from domainmodel.actor import Actor
from domainmodel.genre import Genre
from domainmodel.director import Director


class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.dataset_of_movies: List[Movie] = []
        self.dataset_of_actors: List[Actor] = []
        self.dataset_of_directors: List[Director] = []
        self.dataset_of_genres: List[Genre] = []

    def read_csv_file(self):
        unique_movies: Set[Movie] = set()
        unique_actors: Set[Actor] = set()
        unique_directors: Set[Director] = set()
        unique_genres: Set[Genre] = set()

        with open(self.__file_name, mode='r', encoding='utf-8-sig') as file:
            movie_file_reader = csv.DictReader(file)

            for i, row in enumerate(movie_file_reader):
                title = row['Title']
                genres = [Genre(name) for name in row['Genre'].split(',')]
                description = row['Description']
                director = Director(row['Director'])
                actors = [Actor(name) for name in row['Actors'].split(',')]
                release_year = int(row['Year'])
                runtime_minutes = int(row['Runtime (Minutes)'])
                rating = float(row['Rating'])
                votes = int(row['Votes'])
                revenue_millions = float(row['Revenue (Millions)']) if row['Revenue (Millions)'] != 'N/A' else None
                metascore = int(row['Metascore']) if row['Metascore'] != 'N/A' else None

                movie = Movie(title, release_year)
                movie.genres = genres
                movie.description = description
                movie.director = director
                movie.actors = actors
                movie.runtime_minutes = runtime_minutes

                unique_movies.add(movie)

                for actor in actors:
                    unique_actors.add(actor)

                unique_directors.add(director)

                for genre in genres:
                    unique_genres.add(genre)

        self.dataset_of_movies = list(unique_movies)
        self.dataset_of_actors = list(unique_actors)
        self.dataset_of_directors = list(unique_directors)
        self.dataset_of_genres = list(unique_genres)
