from sqlalchemy import (
    Column,
    String,
    Integer,
    Sequence,
    Float,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import relationship, validates

from models import db


class Movie(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String(80), nullable=False)
    imdb_score = Column(Float, nullable=False)
    director = Column(String(120), nullable=False)
    popularity = Column(Float, nullable=False)

    # Relationships
    genres = relationship(
        "Genre",
        secondary="movies_genres",
        backref=db.backref("movies", lazy="dynamic"),
    )

    def __init__(
        self, name, imdb_score, director, popularity, genres, *args, **kwargs
    ):
        self.name = name
        self.imdb_score = imdb_score
        self.director = director
        self.popularity = popularity
        self.genres = genres

    def __repr__(self):
        return "<Movie - %s, %s>" % (self.name, self.director)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "imdb_score": self.imdb_score,
            "director": self.director,
            "99popularity": self.popularity,
            "genre": [str(genre) for genre in self.genres],
        }

    @validates("name", "director")
    def validate_length(self, key, field):
        if not field:
            raise AssertionError(f"No {key} provided.")
        if len(field) > 80:
            raise AssertionError(f"{key} must be less than 80 characters")
        return field


class Genre(db.Model):
    __tablename__ = "genres"

    id = Column(Integer, Sequence("genre_seq"), primary_key=True)
    name = Column(String(80), unique=True, nullable=False)

    def __init__(self, name, *args, **kwargs):
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class MoviesGenres(db.Model):
    __tablename__ = "movies_genres"

    id = Column(Integer(), primary_key=True)
    movie_id = Column(Integer(), ForeignKey("movies.id", ondelete="CASCADE"))
    genre_id = Column(Integer(), ForeignKey("genres.id", ondelete="CASCADE"))
