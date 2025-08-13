import argparse
import json
import os
import requests
import pandas as pd
from flask import jsonify

parser = argparse.ArgumentParser(description='A CLI for the interaction with an API')

subparsers = parser.add_subparsers(dest='scope', help='Available scopes')



# login
login_parser = subparsers.add_parser('login', help='Login')
login_parser.add_argument('--username', type=str, required=True, help='Username')
login_parser.add_argument('--passw', type=str, required=True, help='Password')

# logout
logout_parser = subparsers.add_parser('logout', help='Logout')
# logout_parser.add_argument('--token', type=str, required=True, help='Token')

#adduser
adduser_parser = subparsers.add_parser('adduser', help='Add user')
adduser_parser.add_argument('--username', type=str, required=True, help='Username')
adduser_parser.add_argument('--passw', type=str, required=True, help='Password')
# adduser_parser.add_argument('--token', type=str, required=True, help='Token')

#user
user_parser = subparsers.add_parser('user',help = 'user')
user_parser.add_argument('--username',type=str, required=True, help = 'Username' )
# user_parser.add_argument('--token', type=str, required=True, help='Token')  

# healthcheck
healthcheck_parser = subparsers.add_parser('healthcheck', help='Check API health')
healthcheck_parser.add_argument('--format', type=str, required=True, help='Format of the response: json or csv')
# healthcheck_parser.add_argument('--token', type=str, required=True, help='Token')

# resetall
resetall_parser = subparsers.add_parser('resetall', help='Reset all questionnaire data')
resetall_parser.add_argument('--format', type=str, required=True, help='Format of the response: json or csv')
# resetall_parser.add_argument('--token', type=str, required=True, help='Token')

# title
title_parser = subparsers.add_parser('title', help='Get title')
title_parser.add_argument('--titleID', type=str, required=True, help='Title id')
# title_parser.add_argument('--token', type=str, required=True, help='Token')

# searchtitle
searchtitle_parser = subparsers.add_parser('searchtitle', help='Search title')
searchtitle_parser.add_argument('--titlepart', type=str, required=True, help='Title')

#name
name_parser = subparsers.add_parser('name', help='Get name')
name_parser.add_argument('--nameID', type=str, required=True, help='Name id')

# searchname
searchname_parser = subparsers.add_parser('searchname', help='Search name')
searchname_parser.add_argument('--name', type=str, required=True, help='Name')

#bygenre
bygenre_parser = subparsers.add_parser('bygenre', help='Get title by genre')
bygenre_parser.add_argument('--genre', type=str, required=True, help='Genre')
bygenre_parser.add_argument('--min', type=str, required=True, help='Minimum rating')

# # questionnaire_upd
# questionnaire_upd_parser = subparsers.add_parser('questionnaire_upd', help='Insert data')
# questionnaire_upd_parser.add_argument('--source', type=argparse.FileType('r'), help='Path to the JSON file')

# # resetq
# resetq_parser = subparsers.add_parser('resetq', help='Reset Questionnaire')
# resetq_parser.add_argument('--questionnaire_id', type=str, required=True, help='Questionnaire id')
# resetq_parser.add_argument('--format', type=str, required=True, help='Format of the response: json or csv')

# # questionnaire
# questionnaire_parser = subparsers.add_parser('questionnaire', help='Get questionnaire')
# questionnaire_parser.add_argument('--questionnaire_id', type=str, required=True, help='Questionnaire id')
# questionnaire_parser.add_argument('--format', type=str, required=True, help='Format of the response: json or csv')

# # question
# question_parser = subparsers.add_parser('question', help='Get question')
# question_parser.add_argument('--questionnaire_id', type=str, required=True, help='Questionnaire id')
# question_parser.add_argument('--question_id', type=str, required=True, help='Question id')
# question_parser.add_argument('--format', type=str, required=True, help='Format of the response: json or csv')

# # doanswer
# doanswer_parser = subparsers.add_parser('doanswer', help='doanswer')
# doanswer_parser.add_argument('--questionnaire_id', type=str, required=True, help='Questionnaire id')
# doanswer_parser.add_argument('--question_id', type=str, required=True, help='Question id')
# doanswer_parser.add_argument('--session_id', type=str, required=True, help='Session id')
# doanswer_parser.add_argument('--option_id', type=str, required=True, help='Option id')

# # getsessionanswers
# getsessionanswers_parser = subparsers.add_parser('getsessionanswers', help='getsessionanswers')
# getsessionanswers_parser.add_argument('--questionnaire_id', type=str, required=True, help='Questionnaire id')
# getsessionanswers_parser.add_argument('--session_id', type=str, required=True, help='Session id')
# getsessionanswers_parser.add_argument('--format', type=str, required=True, help='Format of the response, json or csv')

# # getquestionanswers
# getquestionanswers_parser = subparsers.add_parser('getquestionanswers', help='getquestionanswers')
# getquestionanswers_parser.add_argument('--questionnaire_id', type=str, required=True, help='Questionnaire id')
# getquestionanswers_parser.add_argument('--question_id', type=str, required=True, help='Question id')
# getquestionanswers_parser.add_argument('--format', type=str, required=True, help='Format of the response: json or csv')

args = parser.parse_args()

# login
if args.scope == 'login':
    username = args.username
    passw = args.passw
    url = 'http://localhost:9876/ntuaflix_api/login'
    response = requests.post(url, json={"username": username, "passw": passw})
    print(response.json())
    token = response.json()['token']
    print(token)    
    with open('token.txt', 'w') as f:
        f.write(token)

# read token from file
if os.path.exists('token.txt'):
    with open('token.txt', 'r') as f:
        token = f.read().strip()
else:
    print("No token found. Please login first.")
    exit(1)

    
# logout
if args.scope == 'logout':
    url = 'http://localhost:9876/ntuaflix_api/logout'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(url, headers=headers)
    os.remove('token.txt')
    

# adduser
if args.scope == 'adduser':
    username = args.username
    passw = args.passw
    url = f'http://localhost:9876/ntuaflix_api/admin/usermod/{username}/{passw}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(url, json={"username": username, "passw": passw}, headers=headers)
    print(response.json())

# user
if args.scope == 'user':
    username = args.username
    url = f'http://localhost:9876/ntuaflix_api/admin/users/{username}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers, json={"username": username})
    print(response.json())

# healthcheck
if args.scope == 'healthcheck':
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('http://localhost:9103/ntuaflix_api/admin/healthcheck', headers=headers)
    if args.format == 'json':
        print(response.json())
    elif args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print("Invalid format")
        
# resetall
if args.scope == 'resetall':
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('http://localhost:9103/ntuaflix_api/admin/resetall', headers=headers)
    if args.format == 'json':
        print(response.json())
    elif args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print("Invalid format")

#title
if args.scope == 'title':
    titleID = args.titleID
    url = f'http://localhost:9876/ntuaflix_api/title/{titleID}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers, json={"titleID": titleID})
    print(response.json())

#searchtitle
if args.scope == 'searchtitle':
    titlepart = args.titlepart
    url = f'http://localhost:9876/ntuaflix_api/searchtitle/{titlepart}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers, json={"titlepart": titlepart})
    print(response.json())

#name
if args.scope == 'name':
    nameID = args.nameID
    url = f'http://localhost:9876/ntuaflix_api/name/{nameID}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers, json={"nameID": nameID})
    print(response.json())


#searchname
if args.scope == 'searchname':
    name = args.name
    url = f'http://localhost:9876/ntuaflix_api/searchname/{name}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers, json={"name": name})
    print(response.json())

#bygenre
if args.scope == 'bygenre':
    genre = args.genre
    min = args.min
    url = f'http://localhost:9876/ntuaflix_api/bygenre/'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(url, headers=headers, json={"genre": genre, "min": min})
    print(response.json())


# # questionnaire_udp
# elif args.scope == 'questionnaire_upd':
#     filename = args.source
#     filedata = open(str(filename)[25:-28], 'r') # opens it
#     content = json.load(filedata) # loads it into a dictionary
#     json_object = json.dumps(content, indent=4) # makes it a json again
#     response = requests.post('http://localhost:9103/intelliq_api/admin/questionnaire_upd', json=json_object)
# # resetq
# elif args.scope == 'resetq':
#     url = 'http://localhost:9103/intelliq_api/admin/resetq/{}'.format(args.questionnaire_id)
#     response = requests.post(url)
#     if args.format == 'json':
#         print(response.json())
#     elif args.format == 'csv':
#         df = pd.json_normalize(response.json())
#         df.to_csv()
#         print(df)
#     else:
#         print("Invalid format")
# # questionnaire
# elif args.scope == 'questionnaire':
#     url = 'http://localhost:9103/intelliq_api/questionnaire/{}'.format(args.questionnaire_id)
#     response = requests.get(url)
#     if args.format == 'json':
#         print(response.json())
#     elif args.format == 'csv':
#         df = pd.json_normalize(response.json())
#         df.to_csv()
#         print(df)
#     else:
#         print("Invalid format")
# # question
# elif args.scope == 'question':
#     url = 'http://localhost:9103/intelliq_api/question/{}/{}'.format(args.questionnaire_id, args.question_id)
#     response = requests.get(url)
#     if args.format == 'json':
#         print(response.json())
#     elif args.format == 'csv':
#         df = pd.json_normalize(response.json())
#         df.to_csv()
#         print(df)
#     else:
#         print("Invalid format")
# # doanswer
# elif args.scope == 'doanswer':
#     questionnaire_id = args.questionnaire_id
#     question_id = args.question_id
#     session_id = args.session_id
#     option_id = args.option_id
#     url = 'http://localhost:9103/intelliq_api/doanswer/{}/{}/{}/{}'.format(questionnaire_id, question_id, session_id, option_id)
#     response = requests.post(url)
# # getsessionanswers
# elif args.scope == 'getsessionanswers':
#     url = 'http://localhost:9103/intelliq_api/getsessionanswers/{}/{}'.format(args.questionnaire_id, args.session_id)
#     response = requests.get(url)
#     if args.format == 'json':
#         print(response.json())
#     elif args.format == 'csv':
#         df = pd.json_normalize(response.json())
#         df.to_csv()
#         print(df)
#     else:
#         print("Invalid format")
# elif args.scope == 'getquestionanswers':
#     url = 'http://localhost:9103/intelliq_api/getquestionanswers/{}/{}'.format(args.questionnaire_id, args.question_id)
#     response = requests.get(url)
#     if args.format == 'json':
#         print(response.json())
#     elif args.format == 'csv':
#         df = pd.json_normalize(response.json())
#         df.to_csv()
#         print(df)
#     else:
#         print("Invalid format")
# else:
#     print("Invalid scope")
