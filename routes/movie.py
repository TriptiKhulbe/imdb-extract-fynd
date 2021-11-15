from flask import Blueprint, request

from models.movie import Movie
from services.genre_service import GenreService
from services.movie_service import MovieService
from utils.decorators import token_required

movie = Blueprint("movie", __name__)


@movie.route("/", methods=["GET"])
@token_required(["VIEW_MOVIE"])
def list_movies():
    service = MovieService()
    response = service.list_movies()
    return {
        "status": "success",
        "data": response,
        "message": "",
    }


@movie.route("/", methods=["POST"])
@token_required(["CREATE_MOVIE"])
def add_movie():
    request_args = request.get_json()
    genres = GenreService().merge_genre(request_args.get("genre"))
    movie = Movie(
        name=request_args.get("name"),
        director=request_args.get("director"),
        imdb_score=request_args.get("imdb_score"),
        popularity=request_args.get("99popularity"),
        genres=genres,
    )
    service = MovieService()
    response = service.add_movie(movie)
    return {
        "status": "success",
        "data": response,
        "message": "Movie added.",
    }


@movie.route("/<movie_id>", methods=["PUT"])
@token_required(["EDIT_MOVIE"])
def update_movie(movie_id):
    request_args = request.get_json()
    genres = GenreService().merge_genre(request_args.get("genre"))
    service = MovieService()
    response = service.update_movie(
        movie_id,
        movie_name=request_args.get("name"),
        director=request_args.get("director"),
        imdb_score=request_args.get("imdb_score"),
        popularity=request_args.get("99popularity"),
        genres=genres,
    )
    return {
        "status": "success",
        "data": response,
        "message": "Movie updated.",
    }


@movie.route("/<movie_id>", methods=["DELETE"])
@token_required(["REMOVE_MOVIE"])
def delete_movie(movie_id):
    service = MovieService()
    service.delete_movie(movie_id)
    return {
        "status": "success",
        "data": {},
        "message": "Movie deleted.",
    }


@movie.route("/search", methods=["GET"])
@token_required(["VIEW_MOVIE"])
def search_movies():
    service = MovieService()
    response = service.search_movie(request.args.get("q"))
    return {
        "status": "success",
        "data": response,
        "message": "Search - %s | %d results"
        % (request.args.get("q"), len(response)),
    }
