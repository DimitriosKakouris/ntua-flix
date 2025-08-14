from datetime import timedelta
from io import StringIO
import json
import csv

import requests
from flask import Flask, jsonify, request, Blueprint
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token,jwt_required,get_jwt_identity
from views import get_title as get_title_view


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'bananas'
jwt = JWTManager(app)



# Create a blueprint with the name 'ntuaflx_api', and a url_prefix
ntuaflix_api = Blueprint('ntuaflix_api', __name__, url_prefix='/ntuaflix_api')


@app.route('/ntuaflix_api',methods=['GET'])
@login_required
def home():
    return jsonify({"status":"ok","message":"Welcome to NTUAflix"})


@app.route('/ntuaflix_api/login', methods=['POST'])
def login():
    print("Received a request")
    username = request.json.get('username', None)
    password = request.json.get('passw', None)
    user = db.users.find_one({"username": username})  # query the database for the user

    if user is None or not check_password_hash(user['password'], password):
        response = jsonify({"msg": "Login failed", "redirect": "login"}), 401
        return response

    # user = User(id=1)
    # login_user(user)
     # Create a new token with the user id inside
    access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=30))

    response = jsonify({"msg": "Login successful","token": access_token, "user":username}), 200
    return response

@app.route('/ntuaflix_api/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({}), 200







headers = {
    "accept": "application/json",
    #"Authorization": "Bearer <your_token_here>"
}



# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['local']
collection_users = db['users']
collection_name_basics = db['name_basics']
collection_title_akas = db['title_akas']

collection_title_basics = db['title_basics']
collection_title_crew = db['title_crew']
collection_title_episode = db['title_episode']
collection_title_principals = db['title_principals']
collection_title_ratings = db['title_ratings']
collection_name_test = db['name-test']

@app.route('/ntuaflix_api/admin/usermod/<username>/<password>',methods=['POST'])
def usermod(username,password):
    with app.app_context():
        try:
            user = collection_users.find_one({"username": username})
            hashed_password = generate_password_hash(password)  # hash the password
            if user is None:
                collection_users.insert_one({"username":username,"password":hashed_password})
                return jsonify({"status":"New user created"})
            else:
                collection_users.replace_one({"username":username,"password":hashed_password})
                return jsonify({"status":"Password changed"})

        except Exception as e:
            return jsonify({"status":"error","message":str(e)})


@app.route('/ntuaflix_api/admin/healthcheck',methods=['GET'])
def healthcheck():
    with app.app_context():
        #check if mongodb is connected
        try:
            client.server_info() # will throw an exception
            return jsonify({"status":"ok","dataconnection":True})
        except:
            return jsonify({"status":"error","dataconnection":False})

@app.route('/ntuaflix_api/admin/resetall',methods=['GET'])
def resetall():
    with app.app_context():
        try:
            collection_users.drop()
            collection_name_basics.drop()
            collection_title_akas.drop()
            collection_title_basics.drop()
            collection_title_crew.drop()
            collection_title_episode.drop()
            collection_title_principals.drop()
            collection_title_ratings.drop()
            collection_name_test.drop()
            return jsonify({"status":"ok"})
        except Exception as e:
            return jsonify({"status":"error","message":str(e)})

@app.route('/ntuaflix_api/admin/upload/titlebasics',methods=['POST'])
def upload_titlebasics():
    with app.app_context():
        try:
            # Get the uploaded file
            file = request.files['file']
            # Read the file into a StringIO object
            file_str = StringIO(file.read().decode('utf-8'))

            # Read the .tsv file into a list of dictionaries
            reader = csv.DictReader(file_str, delimiter='\t')
            documents = list(reader)

            # Insert the documents into the collection
            collection_title_basics.insert_many(documents)

            return jsonify({"status":"ok"})
        except BadRequest:
            return jsonify({"status":"error","message":"Bad request. Please upload a .tsv file."})
        except Exception as e:
            return json

@app.route('/ntuaflix_api/admin/upload/titleakas',methods=['POST'])
def upload_titleakas():
    with app.app_context():
        try:
            # Get the uploaded file
            file = request.files['file']
            # Read the file into a StringIO object
            file_str = StringIO(file.read().decode('utf-8'))

            # Read the .tsv file into a list of dictionaries
            reader = csv.DictReader(file_str, delimiter='\t')
            documents = list(reader)

            # Insert the documents into the collection
            collection_title_akas.insert_many(documents)

            return jsonify({"status":"ok"})
        except BadRequest:
            return jsonify({"status":"error","message":"Bad request. Please upload a .tsv file."})
        except Exception as e:
            return json

@app.route('/admin/upload/titlecrew',methods=['POST'])
def upload_titlecrew():
    with app.app_context():
        try:
            # Get the uploaded file
            file = request.files['file']
            # Read the file into a StringIO object
            file_str = StringIO(file.read().decode('utf-8'))

            # Read the .tsv file into a list of dictionaries
            reader = csv.DictReader(file_str, delimiter='\t')
            documents = list(reader)

            # Insert the documents into the collection
            collection_title_crew.insert_many(documents)

            return jsonify({"status":"ok"})
        except BadRequest:
            return jsonify({"status":"error","message":"Bad request. Please upload a .tsv file."})
        except Exception as e:
            return json


@app.route('/ntuaflix_api/admin/upload/titleepisode',methods=['POST'])
def upload_titleepisode():
    with app.app_context():
        try:
            # Get the uploaded file
            file = request.files['file']
            # Read the file into a StringIO object
            file_str = StringIO(file.read().decode('utf-8'))

            # Read the .tsv file into a list of dictionaries
            reader = csv.DictReader(file_str, delimiter='\t')
            documents = list(reader)

            # Insert the documents into the collection
            collection_title_episode.insert_many(documents)

            return jsonify({"status":"ok"})
        except BadRequest:
            return jsonify({"status":"error","message":"Bad request. Please upload a .tsv file."})
        except Exception as e:
            return json

@app.route('/ntuaflix_api/admin/upload/titleprincipals',methods=['POST'])
def upload_titleprincipals():
    with app.app_context():
        try:
            # Get the uploaded file
            file = request.files['file']
            # Read the file into a StringIO object
            file_str = StringIO(file.read().decode('utf-8'))

            # Read the .tsv file into a list of dictionaries
            reader = csv.DictReader(file_str, delimiter='\t')
            documents = list(reader)

            # Insert the documents into the collection
            collection_name_test.insert_many(documents)


            return jsonify({"status":"ok"})
        except BadRequest:
            return jsonify({"status":"error","message":"Bad request. Please upload a .tsv file."})
        except Exception as e:
            return jsonify({"status":"error","message":str(e)})

@app.route('/ntuaflix_api/admin/upload/titleratings',methods=['POST'])

def upload_titleratings():
    with app.app_context():
        try:
            # Get the uploaded file
            file = request.files['file']
            # Read the file into a StringIO object
            file_str = StringIO(file.read().decode('utf-8'))

            # Read the .tsv file into a list of dictionaries
            reader = csv.DictReader(file_str, delimiter='\t')
            documents = list(reader)

            # Insert the documents into the collection
            collection_title_ratings.insert_many(documents)

            return jsonify({"status":"ok"})
        except BadRequest:
            return jsonify({"status":"error","message":"Bad request. Please upload a .tsv file."})
        except Exception as e:
            return json


@app.route('/ntuaflix_api/title/<titleID>', methods=['GET'])

@jwt_required()
def get_title(titleID):
    if not titleID or titleID == 'null' or titleID == 'undefined':
           return {'error': 'Invalid title ID'}, 400
    titleID = str(titleID).strip() if titleID else ""
    return get_title_view(titleID)

@app.route('/ntuaflix_api/seenmovies/', methods=['GET'])
@jwt_required()
def get_seenmovies():
    username = get_jwt_identity()
    results = collection_users.find_one({"username": username})
    if results is not None:
        results = results.get('seenmovies')

        # print(results)
    return jsonify(results)

@app.route('/ntuaflix_api/movie/<titleID>', methods=['GET'])
@jwt_required()
def get_title_selected(titleID):
    return get_title_view(titleID)

@app.route('/ntuaflix_api/searchtitle/<titlepart>', methods=['GET'])
@jwt_required()
def search_title(titlepart):

    url = f"https://api.themoviedb.org/3/search/movie?query={titlepart}&include_adult=false&language=en-US&page=1"
    # Get the query string from the URL
    # query = request.args.get("q")
    response = requests.get(url, headers=headers)

    results = response.json()
    results = results['results']
    # print(len(results))
    results_final=[]
    for i in range(len(results)):
        
        id=results[i].get('id')

        # if results[i].get('media_type') != 'movie':
        #     url = f"https://api.themoviedb.org/3/tv/{id}/external_ids"
        #     response = requests.get(url, headers=headers)
        # elif results[i].get('media_type') != 'tv':
        url = f"https://api.themoviedb.org/3/movie/{id}/external_ids"
        response = requests.get(url, headers=headers)
        # else:
        #     continue
        # print(response.json())
        
        imdb_id = response.json().get('imdb_id')
        if imdb_id is None:
            continue
        results_final.append(imdb_id)

    print(results_final)
    # final_results={
    #     'movie_results'{

    #     }
    # }

    # # Query the title_basics collection
    # results_cursor = collection_title_basics.find({"primaryTitle": {"$regex": query, "$options": "i"}})

    # # Convert the _id fields to strings
    # results = {}
    # for title in results_cursor:
    #     title['_id'] = str(title['_id'])
    #     results[title['_id']] = title

    # Convert the results to JSON and return them
    return jsonify(results_final)


@app.route('/ntuaflix_api/name/<nameID>', methods=['GET'])
@jwt_required()
def get_name(nameID):
    # Query the name_basics collection
    name_basics = collection_name_basics.find_one({"nconst": nameID})
    if name_basics is not None:
        name_basics['_id'] = str(name_basics['_id'])

    name_basics = {"nameID":name_basics.get('_id'), "name": name_basics.get('primaryName'), "birthYear": name_basics.get('birthYear'), "deathYear": name_basics.get('deathYear'), "profession": name_basics.get('primaryProfession'), "nameTitles": name_basics.get('knownForTitles')}

    # Query the title_principals collection
    title_principals_cursor = collection_title_principals.find({"nconst": nameID})

    title_principals_list = []
    for title in title_principals_cursor:
        title['_id'] = str(title['_id'])
        title_principals_list.append({ "tconst": title.get('tconst'), "category": title.get('category')})



    # # Query the title_crew collection
    # title_crew_cursor = collection_title_crew.find({"directors": nameID})

    # # Convert the _id fields to strings
    # title_crew = {}
    # for title in title_crew_cursor:
    #     title['_id'] = str(title['_id'])
    #     title_crew[title['_id']] = title

    # Convert the results to JSON and return them
    return jsonify({
        "name_basics": name_basics,
        "title_principals": title_principals_list,
        # "title_crew": title_crew
    })

@app.route('/ntuaflix_api/searchname/<name>', methods=['GET'])
@jwt_required()
def search_name(name):
    # Get the query string from the URL
    # query = request.args.get("q")
    query = name

    # Query the title_basics collection
    results_cursor = collection_name_basics.find({"primaryName": {"$regex": query, "$options": "i"}})

    # Convert the _id fields to strings
    results = {}
    for title in results_cursor:
        title['_id'] = str(title['_id'])
        results[title['_id']] = title
    # Convert the results to JSON and return them
    print(results)
    return jsonify(list(results))



@app.route('/ntuaflix_api/bygenre',methods=['POST'])
@jwt_required()
def bygenre():
    data = request.get_json()
    genre = data.get("genre")
    minrating = float(data.get("min"))  # Convert minrating to float
    results_cursor = collection_title_basics.find({"genres": {"$regex": genre, "$options": "i"}})

    # Create a list of ids from the results_cursor
    ids = [result['tconst'] for result in results_cursor]

    print(ids)
    # Use the $in operator to find documents where _id is in ids and averageRating is greater than or equal to minrating
    rating_res_cursor = collection_title_ratings.find({"tconst": {"$in": ids}, "averageRating": {"$gte": minrating}})
    ids = [result['tconst'] for result in rating_res_cursor]

    print(ids)

    titleobjects = []
    for i in ids:
        response = get_title_view(i)
        titleobjects.append(response.json)


    return jsonify(titleobjects)


@app.route('/ntuaflix_api/vote',methods=['POST'])
@jwt_required()
def vote():
    data = request.get_json()
    titleID = data.get("titleID")
    rating = float(data.get("rating"))
    user = get_jwt_identity()
    if collection_users.find_one({"username":user,"voted":titleID}) is not None:

        return jsonify({"status":"error","message":"You have already voted for this movie","flag":1})



    curr_numVotes_doc = collection_title_ratings.find_one({"tconst":titleID}, {"numVotes": 1, "_id": 0})
    curr_numVotes = curr_numVotes_doc["numVotes"] if curr_numVotes_doc else 0

    curr_averageRating_doc = collection_title_ratings.find_one({"tconst":titleID}, {"averageRating": 1, "_id": 0})
    curr_averageRating = curr_averageRating_doc["averageRating"] if curr_averageRating_doc else 0.0

    new_averageRating = (curr_averageRating*curr_numVotes+rating)/(curr_numVotes+1)
    collection_title_ratings.update_one({"tconst":titleID},{"$set":{"averageRating":new_averageRating}})
    collection_title_ratings.update_one({"tconst":titleID},{"$inc":{"numVotes":1}})
    collection_users.update_one({"username":user},{"$push":{"voted":titleID}})


    return jsonify({"status":"Vote added"})

if __name__ == '__main__':
    app.run(debug=True,port=9876)
