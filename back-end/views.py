from io import StringIO
import json
import csv
from flask import Flask, jsonify, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import pandas as pd
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['local']
collection_name_basics = db['name_basics']
collection_title_akas = db['title_akas']

collection_title_basics = db['title_basics']
collection_title_crew = db['title_crew']
collection_title_episode = db['title_episode']
collection_title_principals = db['title_principals']
collection_title_ratings = db['title_ratings']
collection_name_test = db['name-test']





def get_title(titleID):
    # Query the title_basics collection
    title_basics = collection_title_basics.find_one({"tconst": titleID})

    # Query the title_akas collection
    title_akas = collection_title_akas.find({"titleId": titleID})

    # Query the title_ratings collection
    title_ratings = collection_title_ratings.find_one({"tconst": titleID})


    if title_basics is not None:
        title_basics['_id'] = str(title_basics['_id'])
        genres = title_basics.get('genres').split(',') if title_basics.get('genres') else []
        title_basics = { "titleID": title_basics.get('tconst'), "type": title_basics.get('titleType'), "originalTitle": title_basics.get('originalTitle'), "titlePoster": title_basics.get('img_url_asset'),"startYear": title_basics.get('startYear'), "endYear":title_basics.get('endYear'), "genres": genres}

    # Query the title_akas collection
    title_akas_cursor = collection_title_akas.find({"titleId": titleID})

    # Convert the _id fields to strings
    title_akas = []
    for title in title_akas_cursor:
        title['_id'] = str(title['_id'])
        title_akas.append({"regionAbbrev": title.get('region'), "akatitle": title.get('title')})
  
    
    # Query the title_ratings collection
    title_ratings = collection_title_ratings.find_one({"tconst": titleID})
    if title_ratings is not None:
        title_ratings['_id'] = str(title_ratings['_id'])
        title_ratings = { "avrating": round(float(title_ratings.get('averageRating')),2), "nvotes": title_ratings.get('numVotes')}
  
    # Query the title_principal collection
    title_principals_cursor = collection_title_principals.find({'tconst': titleID})


    title_principals_list = []
    for doc in title_principals_cursor:
        doc['_id'] = str(doc['_id'])
        name_basics_doc = collection_name_basics.find_one({'nconst': doc['nconst']})
        if name_basics_doc is not None:
            doc['name'] = name_basics_doc['primaryName']
        title_principals_list.append({
            "name": doc.get('name', 'n/a'),
            "nameID": doc.get('nconst'),
            "category": doc.get('category'),
          
        })
    
    # Convert the results to JSON and return them
    return jsonify({
        "titleID": title_basics.get('titleID'),
        "type": title_basics.get('type'),
        "originalTitle": title_basics.get('originalTitle'),
        "titlePoster": title_basics.get('titlePoster'),
        "startYear": title_basics.get('startYear'),
        "endYear": title_basics.get('endYear'),
        "genres": title_basics.get('genres'),
        "titleAkas": title_akas,
        "rating": title_ratings,
        "principals": title_principals_list
    })





def format_handler(res,status,format):
    if format == 'csv':
        df = pd.DataFrame([res])
        return df.to_csv(index=False), status
    else:
        response = jsonify(res), status
        return response

# headers = {
#     "accept": "application/json",
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZjc5YTc3NTY5NDUwYWNkMzFiZWExNzRkYjRkNWY5NyIsInN1YiI6IjY1YTJmMmEwMjY2Nzc4MDEyODY0MjEzMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.n_Z-N--N54d-bWuvwHqlzPgbSQwjNdG9pEszf1mAbSQ"
# }



# def get_title(titleID):
#     url = f"https://api.themoviedb.org/3/find/{titleID}?external_source=imdb_id"

#     # Query the title_basics collection
#     # title_basics = collection_title_basics.find_one({"tconst": titleID})
#     title_basics = requests.get(url, headers=headers)
#     title_basics=title_basics.json()
#     title_basics=title_basics['movie_results'][0]
#     print(title_basics)
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
    # title_ratings = { "avrating": title_basics.get('vote_average'), "nvotes": title_basics.get('vote_count')}

    # # Convert the results to JSON and return them
    # return jsonify({
    #     "title_basics": title_basics,
    #     # "title_akas": title_akas,
    #     "title_ratings": title_ratings
    # })


def get_user_by_id(user_id):
    # Query the users collection
    user = collection_name_test.find_one({"_id": user_id})

    # Convert the _id field to a string
    user['_id'] = str(user['_id'])

    # Return the results
    return user
