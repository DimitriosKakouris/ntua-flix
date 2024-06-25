from datetime import timedelta
from functools import wraps
from io import StringIO
import json
import csv
from bson import ObjectId
from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, get_jwt,jwt_required,get_jwt_identity
from views import get_title as get_title_view
from views import format_handler as format_handler_v

app = Flask(__name__)
app.secret_key = 'bananas'
jwt = JWTManager(app)
blacklist = set()

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





@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklist


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = get_jwt_identity()
        user = collection_users.find_one({"username":username})
        if user['role'] != 'admin':
            return jsonify({"error": "This page is for admins only"}), 403
        return f(*args, **kwargs)
    return decorated_function


@app.route('/ntuaflix_api/protected_endpoint', methods=['POST'])
@jwt_required()
def protected_endpoint():
    return jsonify({}), 200

@app.route('/ntuaflix_api',methods=['GET'])
@jwt_required()
def home():
    format_type = request.args.get('format', 'json')
    data = {"status":"ok","message":"Welcome to NTUAflix"}

    return format_handler_v(data,200,format_type)
   

@app.route('/ntuaflix_api/login', methods=['POST'])
def login():
    format_type = request.args.get('format', 'json')
    username = request.form.get('username', None)
    password = request.form.get('passw', None)

    if username is None or password is None:
        return format_handler_v({"msg": "Missing username or password"},400,format_type)
    
    user = db.users.find_one({"username": username})  # query the database for the user

    if user is None or not check_password_hash(user['password'], password):
        res = {"msg": "Login failed", "redirect": "login"}
        return format_handler_v(res,401,format_type)

     # Create a new token with the user id inside
    access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=30))
   
   
    return format_handler_v({"msg": "Login successful","token": access_token, "user":username}, 200, format_type)

@app.route('/ntuaflix_api/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']  # Get the jti (unique identifier) of the current token
    blacklist.add(jti)
    format_type = request.args.get('format', 'json')
    return format_handler_v({},204,format_type)


@app.route('/ntuaflix_api/admin/usermod/<username>/<password>',methods=['POST'])
@jwt_required()
@admin_required

def usermod(username,password):
    with app.app_context():
        try:
            user = collection_users.find_one({"username": username})
            hashed_password = generate_password_hash(password)  # hash the password
            if user is None:
                collection_users.insert_one({"username":username,"password":hashed_password,"voted":[],"seenmovies":[]})
                res = {"status": "New user created"}
            else:
                collection_users.update_one({"username":username},{"$set":{"password":hashed_password}})
                res = {"status": "Password changed"}
            format_type = request.args.get('format', 'json')
            return format_handler_v(res,200,format_type)
            
        except Exception as e:
            res = {"status": "error", "message": str(e)}
            format_type = request.args.get('format', 'json')
            return format_handler_v(res,500,format_type)


@app.route('/ntuaflix_api/admin/healthcheck',methods=['GET'])
@jwt_required()
@admin_required

def healthcheck():
    with app.app_context():
        #check if mongodb is connected
        try:
            client.server_info() # will throw an exception
            res = {"status": "ok", "dataconnection": 'mongodb://localhost:27017/'}
        except:
            res = {"status": "failed", "dataconnection": 'mongodb://localhost:27017/'}
        
        format_type = request.args.get('format', 'json')
        return format_handler_v(res,200,format_type)
    
@app.route('/ntuaflix_api/admin/resetall',methods=['GET'])
@jwt_required()
@admin_required

def resetall():
    format_type = request.args.get('format', 'json')
    with app.app_context():
        try:
            collection_name_basics.drop()
            collection_title_akas.drop()
            collection_title_basics.drop()
            collection_title_crew.drop()
            collection_title_episode.drop()
            collection_title_principals.drop()
            collection_title_ratings.drop()
            collection_users.drop()

            with open('../data/dbdump/title_basics.json', 'r') as file:
                documents = json.load(file)
             # Convert _id fields to ObjectIDs, if necessary
            for doc in documents:
                if '_id' in doc and not isinstance(doc['_id'], ObjectId):
                    # Assuming the _id field is in the correct format to be converted
                    doc['_id'] = ObjectId(doc['_id']['$oid'])
            collection_title_basics.insert_many(documents)

            with open('../data/dbdump/title_akas.json', 'r') as file:
                documents = json.load(file)
             # Convert _id fields to ObjectIDs, if necessary
            for doc in documents:
                if '_id' in doc and not isinstance(doc['_id'], ObjectId):
                    # Assuming the _id field is in the correct format to be converted
                    doc['_id'] = ObjectId(doc['_id']['$oid'])
            collection_title_akas.insert_many(documents)

            with open('../data/dbdump/title_crew.json', 'r') as file:
                documents = json.load(file)
             # Convert _id fields to ObjectIDs, if necessary
            for doc in documents:
                if '_id' in doc and not isinstance(doc['_id'], ObjectId):
                    # Assuming the _id field is in the correct format to be converted
                    doc['_id'] = ObjectId(doc['_id']['$oid'])
            collection_title_crew.insert_many(documents)

            with open('../data/dbdump/title_episode.json', 'r') as file:
                documents = json.load(file)
             # Convert _id fields to ObjectIDs, if necessary
            for doc in documents:
                if '_id' in doc and not isinstance(doc['_id'], ObjectId):
                    # Assuming the _id field is in the correct format to be converted
                    doc['_id'] = ObjectId(doc['_id']['$oid'])
            collection_title_episode.insert_many(documents)

            with open('../data/dbdump/title_principals.json', 'r') as file:
                documents = json.load(file)
             # Convert _id fields to ObjectIDs, if necessary
            for doc in documents:
                if '_id' in doc and not isinstance(doc['_id'], ObjectId):
                    # Assuming the _id field is in the correct format to be converted
                    doc['_id'] = ObjectId(doc['_id']['$oid'])
            collection_title_principals.insert_many(documents)

            with open('../data/dbdump/title_ratings.json', 'r') as file:
                documents = json.load(file)
             # Convert _id fields to ObjectIDs, if necessary
            for doc in documents:
                if '_id' in doc and not isinstance(doc['_id'], ObjectId):
                    # Assuming the _id field is in the correct format to be converted
                    doc['_id'] = ObjectId(doc['_id']['$oid'])
            collection_title_ratings.insert_many(documents)

            with open('../data/dbdump/name_basics.json', 'r') as file:
                documents = json.load(file)
             # Convert _id fields to ObjectIDs, if necessary
            for doc in documents:
                if '_id' in doc and not isinstance(doc['_id'], ObjectId):
                    # Assuming the _id field is in the correct format to be converted
                    doc['_id'] = ObjectId(doc['_id']['$oid'])
            collection_name_basics.insert_many(documents)


            #Users data was required to be inserted in tsv format
            # Load your documents
            with open('../data/dbdump/users.json', 'r') as file:
                documents = json.load(file)

            # Convert _id fields to ObjectIDs, if necessary
            for doc in documents:
                if '_id' in doc and not isinstance(doc['_id'], ObjectId):
                    # Assuming the _id field is in the correct format to be converted
                    doc['_id'] = ObjectId(doc['_id']['$oid'])

            # Now insert into MongoDB
            collection_users.insert_many(documents)


            # file = open('../data/csvdata/truncated_title.basics.tsv', 'r')
            # # Read the file into a StringIO object
            # file_str = StringIO(file.read())
            # # Read the .tsv file into a list of dictionaries
            # reader = csv.DictReader(file_str, delimiter='\t')
            # documents = list(reader)
            # collection_title_basics.insert_many(documents)

            # file = open('../data/csvdata/truncated_title.akas.tsv', 'r')
            # # Read the file into a StringIO object
            # file_str = StringIO(file.read())
            # # Read the .tsv file into a list of dictionaries
            # reader = csv.DictReader(file_str, delimiter='\t')
            # documents = list(reader)
            # collection_title_akas.insert_many(documents)

            # file = open('../data/csvdata/truncated_title.crew.tsv', 'r')
            # # Read the file into a StringIO object
            # file_str = StringIO(file.read())
            # # Read the .tsv file into a list of dictionaries
            # reader = csv.DictReader(file_str, delimiter='\t')
            # documents = list(reader)
            # collection_title_crew.insert_many(documents)

            # file = open('../data/csvdata/truncated_title.episode.tsv', 'r')
            # # Read the file into a StringIO object
            # file_str = StringIO(file.read())
            # # Read the .tsv file into a list of dictionaries
            # reader = csv.DictReader(file_str, delimiter='\t')
            # documents = list(reader)
            # collection_title_episode.insert_many(documents)

            # file = open('../data/csvdata/truncated_title.principals.tsv', 'r')
            # # Read the file into a StringIO object
            # file_str = StringIO(file.read())
            # # Read the .tsv file into a list of dictionaries
            # reader = csv.DictReader(file_str, delimiter='\t')
            # documents = list(reader)
            # collection_title_principals.insert_many(documents)

            # file = open('../data/csvdata/truncated_title.ratings.tsv', 'r')
            # # Read the file into a StringIO object
            # file_str = StringIO(file.read())
            # # Read the .tsv file into a list of dictionaries
            # reader = csv.DictReader(file_str, delimiter='\t')
            # documents = list(reader)
            # collection_title_ratings.insert_many(documents)

            # file = open('../data/csvdata/truncated_name.basics.tsv', 'r')
            # # Read the file into a StringIO object
            # file_str = StringIO(file.read())
            # # Read the .tsv file into a list of dictionaries
            # reader = csv.DictReader(file_str, delimiter='\t')
            # documents = list(reader)
            # collection_name_basics.insert_many(documents)


            # #Users data was required to be inserted in tsv format
            # # Load your documents
            # with open('../data/dbdump/users.json', 'r') as file:
            #     documents = json.load(file)

            # # Convert _id fields to ObjectIDs, if necessary
            # for doc in documents:
            #     if '_id' in doc and not isinstance(doc['_id'], ObjectId):
            #         # Assuming the _id field is in the correct format to be converted
            #         doc['_id'] = ObjectId(doc['_id']['$oid'])

            # # Now insert into MongoDB
            # collection_users.insert_many(documents)



            
            res = {"status": "ok"}
            return format_handler_v(res,200,format_type)
           
        except Exception as e:
            res = {"status": "failed", "message": str(e)}
            return format_handler_v(res,500,format_type)
           

@app.route('/ntuaflix_api/admin/upload/titlebasics',methods=['POST'])
@jwt_required()
@admin_required

def upload_titlebasics():
    format_type = request.args.get('format', 'json')
    with app.app_context():
        try:
            # Get the uploaded file
            file = request.files['file']
            # Read the file into a StringIO object
            file_str = StringIO(file.read().decode('utf-8'))

            # Read the .tsv file into a list of dictionaries
            reader = csv.DictReader(file_str, delimiter='\t')
            documents = list(reader)
            collection_title_basics.insert_many(documents)


            res={"status":"ok"}
            return format_handler_v(res,200,format_type)
            
        except BadRequest:
            res = {"status": "error", "message": "Bad request. Please upload a .tsv file."}
            return format_handler_v(res,400,format_type)
        

@app.route('/ntuaflix_api/admin/upload/titleakas',methods=['POST'])
@jwt_required()
@admin_required

def upload_titleakas():
    with app.app_context():
        format_type = request.args.get('format', 'json')
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

            res={"status":"ok"}
            return format_handler_v(res,200,format_type)
           
        except BadRequest:
            res = {"status": "error", "message": "Bad request. Please upload a .tsv file."}
            return format_handler_v(res,400,format_type)
     


@app.route('/ntuaflix_api/admin/upload/namebasics',methods=['POST'])
@jwt_required()
@admin_required

def upload_namebasics():
    with app.app_context():
        format_type = request.args.get('format', 'json')
        try:
            # Get the uploaded file
            file = request.files['file']
            # Read the file into a StringIO object
            file_str = StringIO(file.read().decode('utf-8'))

            # Read the .tsv file into a list of dictionaries
            reader = csv.DictReader(file_str, delimiter='\t')
            documents = list(reader)

            # Insert the documents into the collection
            collection_name_basics.insert_many(documents)

            res={"status":"ok"}
            return format_handler_v(res,200,format_type)
           
        except BadRequest:
            res = {"status": "error", "message": "Bad request. Please upload a .tsv file."}
            return format_handler_v(res,400,format_type)
        
@app.route('/ntuaflix_api/admin/upload/titlecrew',methods=['POST'])
@jwt_required()
@admin_required

def upload_titlecrew():
    with app.app_context():
        format_type = request.args.get('format', 'json')
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


            return format_handler_v({"status":"ok"},200,format_type)
        except BadRequest:
            return format_handler_v({"status":"error","message":"Bad request. Please upload a .tsv file."},400,format_type)
        

@app.route('/ntuaflix_api/admin/upload/titleepisode',methods=['POST'])
@jwt_required()
@admin_required

def upload_titleepisode():
    with app.app_context():
        format_type = request.args.get('format', 'json')
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


            return format_handler_v({"status":"ok"},200,format_type)
        except BadRequest:
            return format_handler_v({"status":"error","message":"Bad request. Please upload a .tsv file."},400,format_type)
        
        
@app.route('/ntuaflix_api/admin/upload/titleprincipals',methods=['POST'])
@jwt_required()
@admin_required

def upload_titleprincipals():
    with app.app_context():
        format_type = request.args.get('format', 'json')
        try:
            # Get the uploaded file
            file = request.files['file']
            # Read the file into a StringIO object
            file_str = StringIO(file.read().decode('utf-8'))

            # Read the .tsv file into a list of dictionaries
            reader = csv.DictReader(file_str, delimiter='\t')
            documents = list(reader)

            # Insert the documents into the collection
            collection_title_principals.insert_many(documents)


            return format_handler_v({"status":"ok"},200,format_type)
        except BadRequest:
            return format_handler_v({"status":"error","message":"Bad request. Please upload a .tsv file."},400,format_type)
       


@app.route('/ntuaflix_api/admin/upload/titleratings',methods=['POST'])
@jwt_required()
@admin_required

def upload_titleratings():
    with app.app_context():
        format_type = request.args.get('format', 'json')
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

            return format_handler_v({"status":"ok"},200,format_type)
        except BadRequest:
            return format_handler_v({"status":"error","message":"Bad request. Please upload a .tsv file."},400,format_type)
      

@app.route('/ntuaflix_api/admin/users/<username>',methods=['GET'])
@jwt_required()
@admin_required
def get_user_info(username):
    format_type = request.args.get('format', 'json')
    user = collection_users.find_one({"username":username})
    if user is not None:
        user.pop('_id')
        user.pop('password')
        return format_handler_v(user,200,format_type)
    else:
        return format_handler_v({"status":"error","message":"User not found"},400,format_type)



@app.route('/ntuaflix_api/title/<titleID>', methods=['GET'])
@jwt_required()
def get_title(titleID):
    return get_title_view(titleID)



@app.route('/ntuaflix_api/seenmovies', methods=['GET'])
@jwt_required()
def get_seenmovies():
    format_type = request.args.get('format', 'json')
    username = get_jwt_identity()
    results = collection_users.find_one({"username": username})
    if results is not None:
        results = results.get('seenmovies')
        return format_handler_v(results,200,format_type)

    else:
        results = []
        return format_handler_v(results,204,format_type)
       
       

@app.route('/ntuaflix_api/searchtitle', methods=['GET'])
@jwt_required()
def search_title():
    format_type = request.args.get('format', 'json')

    # Get the raw data from the request body
    body_data = request.get_data()

    # Parse the JSON data from the request body
    body_json = json.loads(body_data)

    # Get the titlePart from the parsed JSON
    titlePart = str(body_json.get("titlePart"))

    if titlePart == "":
        return format_handler_v({},204,format_type)
    

    # Query the title_basics collection
    results_cursor = collection_title_basics.find({"originalTitle": {"$regex": titlePart, "$options": "i"}})

    # Convert the _id fields to strings
    results = {}
    for title in results_cursor:
        title['_id'] = str(title['_id'])
        results[title['_id']] = title

    if len(results) == 0:
        return format_handler_v({},400,format_type)
    
    else:
        return format_handler_v(results,200,format_type)



@app.route('/ntuaflix_api/searchtitlealias', methods=['POST'])
@jwt_required()
def search_titlefull():
    format_type = request.args.get('format', 'json')

    titlePart = request.json.get("titlePart")

    if titlePart == "":
        return format_handler_v({},204,format_type)
    
    # Query the title_basics collection
    results_cursor = collection_title_basics.find({"originalTitle": {"$regex": titlePart, "$options": "i"}})

    # Convert the _id fields to strings
    results = {}
    for title in results_cursor:
        title['_id'] = str(title['_id'])
        results[title['_id']] = title
    
    if len(results) == 0:
        return format_handler_v({},204,format_type)
    
    else:
        return format_handler_v(results,200,format_type)



@app.route('/ntuaflix_api/name/<nameID>', methods=['GET'])
@jwt_required()
def get_name(nameID):
    # Query the name_basics collection
    format_type = request.args.get('format', 'json')
    name_basics = collection_name_basics.find_one({"nconst": nameID})
    if name_basics is not None:
        name_basics['_id'] = str(name_basics['_id'])
    
    # Query the title_principals collection
    title_principals_cursor = collection_title_principals.find({"nconst": nameID})

    nameTitles = []
    for title in title_principals_cursor:
        title['_id'] = str(title['_id'])
        nameTitles.append({ "titleID": title.get('tconst'), "category": title.get('category')})

    # Convert the results to JSON and return them
    res = {"nameID":name_basics.get('nconst'), "name": name_basics.get('primaryName'), "namePoster":name_basics.get('img_url_asset'), "birthYear": name_basics.get('birthYear'), "deathYear": name_basics.get('deathYear'), "profession": name_basics.get('primaryProfession'),"nameTitles": nameTitles}
        
    return format_handler_v(res,200,format_type)

@app.route('/ntuaflix_api/searchname', methods=['GET'])
@jwt_required()
def search_name():
    format_type = request.args.get('format', 'json')
    # Get the raw data from the request body
    body_data = request.get_data()

    # Parse the JSON data from the request body
    body_json = json.loads(body_data)

    # Get the titlePart from the parsed JSON
    query = str(body_json.get("namePart"))

    if query == "":
        return format_handler_v({},400,format_type)
    

    # Query the title_basics collection
    results_cursor = collection_name_basics.find({"primaryName": {"$regex": query, "$options": "i"}})

    # Convert the _id fields to strings
    results = {}
    for title in results_cursor:
        title['_id'] = str(title['_id'])
        results[title['_id']] = title
    
    if len(results) == 0:
        return format_handler_v({},204,format_type)
    
    else:
        return format_handler_v(results,200,format_type)


@app.route('/ntuaflix_api/tvepisode/<titleID>',methods=['GET'])
@jwt_required()
def get_tvepisode(titleID):
    format_type = request.args.get('format', 'json')
    # Query the title_episode collection
    title_episode = collection_title_episode.find_one({"tconst": titleID})
    if title_episode is not None:
        title_episode['_id'] = str(title_episode['_id'])
        title_episode = {"titleID": title_episode.get('tconst'), "season": title_episode.get('seasonNumber'), "episode": title_episode.get('episodeNumber')}
    
    return format_handler_v(title_episode,200,format_type)




@app.route('/ntuaflix_api/bygenre',methods=['GET'])
@jwt_required()
def bygenre():
    format_type = request.args.get('format', 'json')

    # Get the raw data from the request body
    body_data = request.get_data()

    # Parse the JSON data from the request body
    body_json = json.loads(body_data)

    # Get the titlePart from the parsed JSON
    qgenre = str(body_json.get("qgenre"))
    minrating = str(body_json.get("minrating"))  # Convert minrating to float

    if qgenre == "" or qgenre==None or minrating is None:
        return format_handler_v({},400,format_type)

    results_cursor = collection_title_basics.find({"genres": {"$regex": qgenre, "$options": "i"}})

    
    # Create a list of ids from the results_cursor
    ids = [result['tconst'] for result in results_cursor]
  
   
    # Use the $in operator to find documents where _id is in ids and averageRating is greater than or equal to minrating
    rating_res_cursor = collection_title_ratings.find({"tconst": {"$in": ids}, "averageRating": {"$gte": minrating}})
    ids = [result['tconst'] for result in rating_res_cursor]
  
    
    titleobjects = []
    for i in ids:
        response = get_title_view(i)
        titleobjects.append(response.json)
    
    if len(titleobjects) == 0:
            return format_handler_v([],204,format_type)
    else:
        return format_handler_v(titleobjects,200,format_type)
    




@app.route('/ntuaflix_api/bygenrealias',methods=['POST'])
@jwt_required()
def bygenrealias():
    format_type = request.args.get('format', 'json')

    qgenre = str(request.json.get("qgenre"))
    if qgenre == "" or qgenre == None:
        return format_handler_v({},400,format_type)

    results_cursor = collection_title_basics.find({"genres": {"$regex": qgenre, "$options": "i"}})

    # Convert the _id fields to strings
    results = {}
    for title in results_cursor:
        title['_id'] = str(title['_id'])
        results[title['_id']] = title
  
    if len(results) == 0:
        return format_handler_v({},204,format_type)
    else:
        return format_handler_v(results,200,format_type)
    
@app.route('/ntuaflix_api/vote',methods=['POST'])
@jwt_required()
def vote():
    format_type = request.args.get('format', 'json')
    data = request.get_json()
    titleID = data.get("titleID")
    rating =float(data.get("rating"))
    if titleID == "" or titleID == None or rating == "" or rating == None:
        return format_handler_v({"status":"failed","message":"Bad request. Please provide a titleID and a rating."},400,format_type)
    
    user = get_jwt_identity()
    if collection_users.find_one({"username":user,"voted":titleID}) is not None:
       
       return format_handler_v({"status":"failed","message":"You have already voted for this movie","flag":1},200,format_type)

   
    curr_numVotes_doc = collection_title_ratings.find_one({"tconst":titleID}, {"numVotes": 1, "_id": 0})
    curr_numVotes = float(curr_numVotes_doc["numVotes"] if curr_numVotes_doc else 0)

    curr_averageRating_doc = collection_title_ratings.find_one({"tconst":titleID}, {"averageRating": 1, "_id": 0})
    curr_averageRating = float(curr_averageRating_doc["averageRating"]) if curr_averageRating_doc else 0.0

    if curr_averageRating == 'n/a':
        return format_handler_v({"status":"failed","message":"Movie has no rating","flag":1},200,format_type)
    
    new_averageRating = (curr_averageRating*curr_numVotes+rating)/(curr_numVotes+1)

    # Convert numVotes to an integer, increment it, and convert it back to a string
    new_numVotes = str(int(curr_numVotes) + 1) 

    collection_title_ratings.update_one({"tconst":titleID},{"$set":{"averageRating":new_averageRating}})
    collection_title_ratings.update_one({"tconst":titleID},{"$set": {"numVotes": new_numVotes}})
    collection_users.update_one({"username":user},{"$push":{"voted":titleID}})

   
    return format_handler_v({"status":"ok","message":"Vote submitted successfully","flag":0},200,format_type)




if __name__ == '__main__':
    app.run(host="localhost",debug=True,port=9876)


