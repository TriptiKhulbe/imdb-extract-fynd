import logging

from models import db
from models.movie import Genre


class GenreService:
    def __init__(self):
        self.log = logging.getLogger(__class__.__name__)

    def list_genre(self):
        genres = []
        for genre in db.session.query(Genre):
            genre.append(genre.to_dict())
        return {"genres": genres}

    def merge_genre(self, genres):
        genres_found = (
            db.session.query(Genre).filter(Genre.name.in_(genres)).all()
        )
        genres_new = [
            Genre(name)
            for name in set(genres).difference(
                set(map(lambda x: str(x), genres_found))
            )
        ]
        db.session.add_all(genres_new)
        return genres_new + genres_found
