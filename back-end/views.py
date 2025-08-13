from io import StringIO
import json
import csv

import requests
from flask import Flask, jsonify, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token
from webbrowser import get

# from ntuaflix.back-end.app import get_name

# # Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017/')
# db = client['local']
# collection_name_basics = db['name_basics']
# collection_title_akas = db['title_akas']

# collection_title_basics = db['title_basics']
# collection_title_crew = db['title_crew']
# collection_title_episode = db['title_episode']
# collection_title_principals = db['title_principals']
# collection_title_ratings = db['title_ratings']
# collection_name_test = db['name-test']





# def get_title(titleID):
#     # Query the title_basics collection
#     title_basics = collection_title_basics.find_one({"tconst": titleID})

#     # Query the title_akas collection
#     title_akas = collection_title_akas.find({"titleId": titleID})

#     # Query the title_ratings collection
#     title_ratings = collection_title_ratings.find_one({"tconst": titleID})

#     if title_basics is not None:
#         title_basics['_id'] = str(title_basics['_id'])

#     # Query the title_akas collection
#     title_akas_cursor = collection_title_akas.find({"titleId": titleID})

#     # Convert the _id fields to strings
#     title_akas = []
#     for title in title_akas_cursor:
#         title['_id'] = str(title['_id'])
#         title_akas.append({"regionAbbrev": title.get('region'), "akatitle": title.get('title')})


#     # Query the title_ratings collection
#     title_ratings = collection_title_ratings.find_one({"tconst": titleID})
#     if title_ratings is not None:
#         title_ratings['_id'] = str(title_ratings['_id'])
#         title_ratings = { "avrating": round(title_ratings.get('averageRating'),2), "nvotes": title_ratings.get('numVotes')}

#     # Convert the results to JSON and return them
#     return jsonify({
#         "title_basics": title_basics,
#         "title_akas": title_akas,
#         "title_ratings": title_ratings
#     })




headers = {
    "accept": "application/json",
    # "Authorization": "Put API KEY here"
}



def get_title(titleID):
    url_imdb = f"https://api.themoviedb.org/3/find/{titleID}?external_source=imdb_id"

    id_moviedb = requests.get(url_imdb,headers=headers)

    id_moviedb = id_moviedb.json()

    titleID= id_moviedb['movie_results'][0]['id']

    url = f"https://api.themoviedb.org/3/movie/{titleID}?language=en-US"
# Query the title_basics collection
# title_basics = collection_title_basics.find_one({"tconst": titleID})

    title_basics = requests.get(url, headers=headers)
    title_basics = title_basics.json()
# print(title_basics)
# if not title_basics[0]:
#     print("No movie results found for the given titleID")
#     return jsonify({})


# print(title_basics)
# # Query the title_akas collection
# title_akas = collection_title_akas.find({"titleId": titleID})

# # Query the title_ratings collection
# title_ratings = collection_title_ratings.find_one({"tconst": titleID})


# if title_basics is not None:
#     title_basics['id'] = str(title_basics['id'])

# # Query the title_akas collection
# title_akas_cursor = collection_title_akas.find({"titleId": titleID},{"isOriginalTitle": 0})

# # Convert the _id fields to strings
# title_akas = []
# for title in title_akas_cursor:
#     title['_id'] = str(title['_id'])
#     title_akas.append({"regionAbbrev": title.get('region'), "akatitle": title.get('title')})
# title_akas = { "nvotes": title_ratings.get('vote_count')}

# # Query the title_ratings collection
# title_ratings = collection_title_ratings.find_one({"tconst": titleID})
# if title_ratings is not None:
#     title_ratings['_id'] = str(title_ratings['_id'])
#
    title_genre = title_basics.get('genres')[0].get('name')
    title_ratings = { "avrating": title_basics.get('vote_average'), "nvotes": title_basics.get('vote_count')}
    print(title_basics)
    # Convert the results to JSON and return them
    return jsonify({
        "title_basics": title_basics,
        "title_genre": title_genre,
        "title_ratings": title_ratings
    })


# def get_user_by_id(user_id):
#     # Query the users collection
#     user = collection_name_test.find_one({"_id": user_id})

#     # Convert the _id field to a string
#     user['_id'] = str(user['_id'])

#     # Return the results
#     return user
