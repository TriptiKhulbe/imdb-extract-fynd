from unittest import TestCase
from unittest.mock import patch

from models.movie import Movie, Genre
from services.movie_service import MovieService


class TestMovieService(TestCase):
    def setUp(self) -> None:
        self.db = patch("services.movie_service.db").start()
        self.g1 = Genre("g1")
        self.g2 = Genre("g2")
        self.g3 = Genre("g3")
        self.m1 = Movie(
            name="m1",
            director="d1",
            imdb_score=1.1,
            popularity=90,
            genres=[self.g1, self.g2],
        )
        self.m1.id = 1

        self.m2 = Movie(
            name="m2",
            director="d2",
            imdb_score=2.2,
            popularity=90,
            genres=[self.g2, self.g3],
        )
        self.m2.id = 2
        self.addCleanup(patch.stopall)

    def test_list_movies(self):
        self.db.session.query.return_value = [self.m1, self.m2]
        service = MovieService()
        actual = service.list_movies()
        expected = [
            {
                "id": 1,
                "name": "m1",
                "imdb_score": 1.1,
                "director": "d1",
                "99popularity": 90,
                "genre": ["g1", "g2"],
            },
            {
                "id": 2,
                "name": "m2",
                "imdb_score": 2.2,
                "director": "d2",
                "99popularity": 90,
                "genre": ["g2", "g3"],
            },
        ]
        assert actual == expected

    def test_add_movie(self):
        service = MovieService()
        actual = service.add_movie(self.m1)
        expected = {
            "id": 1,
            "name": "m1",
            "imdb_score": 1.1,
            "director": "d1",
            "99popularity": 90,
            "genre": ["g1", "g2"],
        }
        assert actual == expected

    def test_delete_movie(self):
        self.db.session.query.return_value.filter.return_value.first.return_value = (
            self.m1
        )
        service = MovieService()
        service.delete_movie(movie_id=1)
        self.db.session.delete.assert_called_with(self.m1)

    def test_update_movie(self):
        self.db.session.query.return_value.filter.return_value.first.return_value = (
            self.m1
        )
        service = MovieService()
        actual = service.update_movie(
            1,
            movie_name="m1",
            director="d_new_1",
            imdb_score=9.9,
            popularity=45,
            genres=[self.g1, self.g2, self.g3],
        )
        expected = {
            "id": 1,
            "name": "m1",
            "imdb_score": 9.9,
            "director": "d_new_1",
            "99popularity": 45,
            "genre": ["g1", "g2", "g3"],
        }
        assert actual == expected
