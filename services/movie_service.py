import logging

from sqlalchemy import or_

from models import db
from models.movie import Movie, Genre, MoviesGenres


class MovieService:
    def __init__(self):
        self.log = logging.getLogger(__class__.__name__)

    def list_movies(self):
        movies = []
        for movie in db.session.query(Movie):
            movies.append(movie.to_dict())
        return movies

    def add_movie(self, movie: Movie):
        db.session.add(movie)
        db.session.commit()
        return movie.to_dict()

    def delete_movie(self, movie_id):
        movie = db.session.query(Movie).filter(Movie.id == movie_id).first()
        db.session.delete(movie)
        db.session.commit()

    def update_movie(
        self, movie_id, *, movie_name, director, popularity, imdb_score, genres
    ):
        movie = db.session.query(Movie).filter(Movie.id == movie_id).first()
        movie.name = movie_name
        movie.director = director
        movie.popularity = popularity
        movie.imdb_score = imdb_score
        movie.genres = genres
        db.session.commit()
        return movie.to_dict()

    def search_movie(self, text: str):
        search = "%{}%".format(text)
        movies = (
            db.session.query(Movie)
            .join(MoviesGenres, MoviesGenres.movie_id == Movie.id)
            .join(Genre, Genre.id == MoviesGenres.genre_id)
            .filter(
                or_(
                    Movie.name.like(search),
                    Movie.director.like(search),
                    Genre.name.like(search),
                )
            )
            .all()
        )
        return [movie.to_dict() for movie in movies]
