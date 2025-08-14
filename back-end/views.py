from io import StringIO
import requests
from flask import Flask, jsonify, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token
from webbrowser import get




headers = {
    "accept": "application/json",
    #"Authorization": "Bearer <your_token_here>"
}



def get_title(titleID):
    url_imdb = f"https://api.themoviedb.org/3/find/{titleID}?external_source=imdb_id"
    id_moviedb = requests.get(url_imdb, headers=headers).json()

    # Try to get movie or TV show ID
    movie_results = id_moviedb.get('movie_results', [])
    tv_results = id_moviedb.get('tv_results', [])

    title_basics = {}

    if movie_results:
        movie_id = movie_results[0]['id']
        url_movie = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
        title_basics = requests.get(url_movie, headers=headers).json()
    if tv_results:
        tv_id = tv_results[0]['id']
        url_tv = f"https://api.themoviedb.org/3/tv/{tv_id}?language=en-US"
        tv_basics = requests.get(url_tv, headers=headers).json()
        # Combine TV show info into title_basics (movie info takes precedence)
        print(tv_basics)
        title_basics.update(tv_basics)


    if title_basics.get('genres') not in [None, []]:
        title_genre = title_basics.get('genres')[0].get('name')
    else:
        title_genre = "N/A"

    title_ratings = { "avrating": round(title_basics.get('vote_average'), 1), "nvotes": title_basics.get('vote_count') }
    print(title_basics)
    # Convert the results to JSON and return them
    return jsonify({
        "title_basics": title_basics,
        "title_genre": title_genre,
        "title_ratings": title_ratings
    })
