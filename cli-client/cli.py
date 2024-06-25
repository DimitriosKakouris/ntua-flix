import argparse
import json
import os
import requests
import pandas as pd
from flask import jsonify



# Create a parent parser with 'seng2339' as an argument
parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('se2339', help='Prefix for every command')

parser = argparse.ArgumentParser(description='A CLI for the interaction with an API',parents=[parent_parser])

subparsers = parser.add_subparsers(dest='scope', help='Available scopes')



# login
login_parser = subparsers.add_parser('login', help='Login')
login_parser.add_argument('--username', type=str, required=True, help='Username')
login_parser.add_argument('--passw', type=str, required=True, help='Password')
login_parser.add_argument('--format', default="json",type=str, required=False, help='Format of the response: json or csv')

# logout
logout_parser = subparsers.add_parser('logout', help='Logout')

# logout_parser.add_argument('--token', type=str, required=True, help='Token')

#adduser
adduser_parser = subparsers.add_parser('adduser', help='Add user')
adduser_parser.add_argument('--username', type=str, required=True, help='Username')
adduser_parser.add_argument('--passw', type=str, required=True, help='Password')
adduser_parser.add_argument('--format', default="json",type=str, required=False, help='Format of the response: json or csv')
# adduser_parser.add_argument('--token', type=str, required=True, help='Token')

#user
user_parser = subparsers.add_parser('user',help = 'user')
user_parser.add_argument('--username',type=str, required=True, help = 'Username' )
user_parser.add_argument('--format', default="json",type=str, required=False, help='Format of the response: json or csv')
# user_parser.add_argument('--token', type=str, required=True, help='Token')  

# healthcheck
healthcheck_parser = subparsers.add_parser('healthcheck', help='Check API health')
healthcheck_parser.add_argument('--format', default="json", type=str, required=False, help='Format of the response: json or csv')
# healthcheck_parser.add_argument('--token', type=str, required=True, help='Token')

# resetall
resetall_parser = subparsers.add_parser('resetall', help='Reset all questionnaire data')
resetall_parser.add_argument('--format', default="json",type=str, required=False, help='Format of the response: json or csv')
# resetall_parser.add_argument('--token', type=str, required=True, help='Token')

#newtitles
newtitles_parser = subparsers.add_parser('newtitles', help='Upload title basics')
newtitles_parser.add_argument('--filename', type=argparse.FileType('r'), help='Path to the JSON file')
newtitles_parser.add_argument('--format', default="json",required=False, help='Format of the response: json or csv')


#newcrew
newcrew_parser = subparsers.add_parser('newcrew', help='Upload title crew')
newcrew_parser.add_argument('--filename', type=argparse.FileType('r'), help='Path to the JSON file')
newcrew_parser.add_argument('--format',default="json", required=False, help='Format of the response: json or csv')

#newakas
newakas_parser = subparsers.add_parser('newakas', help='Upload title akas')
newakas_parser.add_argument('--filename', type=argparse.FileType('r'), help='Path to the JSON file')
newakas_parser.add_argument('--format',default="json", required=False, help='Format of the response: json or csv')

#newnames
newnames_parser = subparsers.add_parser('newnames', help='Upload name basics')
newnames_parser.add_argument('--filename', type=argparse.FileType('r'), help='Path to the JSON file')
newnames_parser.add_argument('--format',default="json", required=False, help='Format of the response: json or csv')


#newepisode
newepisode_parser = subparsers.add_parser('newepisode', help='Upload title episode')
newepisode_parser.add_argument('--filename', type=argparse.FileType('r'), help='Path to the JSON file')
newepisode_parser.add_argument('--format',default="json", required=False, help='Format of the response: json or csv')


#newprincipals
newprincipals_parser = subparsers.add_parser('newprincipals', help='Upload title principals')
newprincipals_parser.add_argument('--filename', type=argparse.FileType('r'), help='Path to the JSON file')
newprincipals_parser.add_argument('--format',default="json",required=False, help='Format of the response: json or csv')

#newratings
newratings_parser = subparsers.add_parser('newratings', help='Upload title ratings')
newratings_parser.add_argument('--filename', type=argparse.FileType('r'), help='Path to the JSON file')
newratings_parser.add_argument('--format',default="json", required=False, help='Format of the response: json or csv')


# title
title_parser = subparsers.add_parser('title', help='Get title')
title_parser.add_argument('--titleID', type=str, required=True, help='Title id')
title_parser.add_argument('--format',default="json", required=False, help='Format of the response: json or csv')

# searchtitle
searchtitle_parser = subparsers.add_parser('searchtitle', help='Search title')
searchtitle_parser.add_argument('--titlepart', type=str, required=True, help='Title')
searchtitle_parser.add_argument('--format',default="json", required=False, help='Format of the response: json or csv')

#name
name_parser = subparsers.add_parser('name', help='Get name')
name_parser.add_argument('--nameid', type=str, required=True, help='Name id')
name_parser.add_argument('--format',default="json", required=False, help='Format of the response: json or csv')

# searchname
searchname_parser = subparsers.add_parser('searchname', help='Search name')
searchname_parser.add_argument('--name', type=str, required=True, help='Name')
searchname_parser.add_argument('--format',default="json", required=False, help='Format of the response: json or csv')

#bygenre
bygenre_parser = subparsers.add_parser('bygenre', help='Get title by genre')
bygenre_parser.add_argument('--genre', type=str, required=True, help='Genre')
bygenre_parser.add_argument('--min', type=str, required=True, help='Minimum rating')
bygenre_parser.add_argument('--format',default="json", required=False, help='Format of the response: json or csv')


args = parser.parse_args()

# login
if args.scope == 'login':
    username = args.username
    passw = args.passw
    url = 'http://localhost:9876/ntuaflix_api/login'
    response = requests.post(url, data={"username": username, "passw": passw})
    print(response.json())
    if response.status_code == 401:
        print("Invalid username or password")
        exit(1)
    else:
        token = response.json()['token']
        
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
    if args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print(response.json())

# users
if args.scope == 'user':
    username = args.username
    url = f'http://localhost:9876/ntuaflix_api/admin/users/{username}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers, json={"username": username})
    if args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print(response.json())

# healthcheck
if args.scope == 'healthcheck':
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get('http://localhost:9876/ntuaflix_api/admin/healthcheck', headers=headers)
    if args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print(response.json())
   
# resetall
if args.scope == 'resetall':
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('http://localhost:9876/ntuaflix_api/admin/resetall', headers=headers)


    if args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print(response.json())
   

#newtitles
if args.scope == 'newtitles':
    filedata = args.filename
    

    url = f'http://localhost:9876/ntuaflix_api/admin/upload/titlebasics'
    headers = {'Authorization': f'Bearer {token}'}
    files = {'file': filedata}  # File to be sent
    response = requests.post(url, headers=headers, files=files)
    filedata.close()  # Close the file

    if args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print(response.json())

#newcrew
if args.scope == 'newcrew':
    filedata = args.filename
    

    url = f'http://localhost:9876/ntuaflix_api/admin/upload/titlecrew'
    headers = {'Authorization': f'Bearer {token}'}
    files = {'file': filedata}  # File to be sent
    response = requests.post(url, headers=headers, files=files)
    filedata.close()  # Close the file

    if args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print(response.json())

#newakas
if args.scope == 'newakas':
    filedata = args.filename
    

    url = f'http://localhost:9876/ntuaflix_api/admin/upload/titleakas'
    headers = {'Authorization': f'Bearer {token}'}
    files = {'file': filedata}  # File to be sent
    response = requests.post(url, headers=headers, files=files)
    filedata.close()  # Close the file

    if args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print(response.json())

#newnames
if args.scope == 'newnames':
    filedata = args.filename
    

    url = f'http://localhost:9876/ntuaflix_api/admin/upload/namebasics'
    headers = {'Authorization': f'Bearer {token}'}
    files = {'file': filedata}  # File to be sent
    response = requests.post(url, headers=headers, files=files)
    filedata.close()  # Close the file

    if args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print(response.json())

#newepisode
if args.scope == 'newepisode':
    filedata = args.filename
    

    url = f'http://localhost:9876/ntuaflix_api/admin/upload/titleepisode'
    headers = {'Authorization': f'Bearer {token}'}
    files = {'file': filedata}  # File to be sent
    response = requests.post(url, headers=headers, files=files)
    filedata.close()  # Close the file

    if args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print(response.json())

#newprincipals
if args.scope == 'newprincipals':
    filedata = args.filename
    

    url = f'http://localhost:9876/ntuaflix_api/admin/upload/titleprincipals'
    headers = {'Authorization': f'Bearer {token}'}
    files = {'file': filedata}  # File to be sent
    response = requests.post(url, headers=headers, files=files)
    filedata.close()  # Close the file

    if args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print(response.json())

#newratings
if args.scope == 'newratings':
    filedata = args.filename
    

    url = f'http://localhost:9876/ntuaflix_api/admin/upload/titleratings'
    headers = {'Authorization': f'Bearer {token}'}
    files = {'file': filedata}  # File to be sent
    response = requests.post(url, headers=headers, files=files)
    filedata.close()  # Close the file

    if args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print(response.json())


#title
if args.scope == 'title':
    titleID = args.titleID
    url = f'http://localhost:9876/ntuaflix_api/title/{titleID}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print(response.json())

#searchtitle
if args.scope == 'searchtitle':
    titlepart = args.titlepart
    url = f'http://localhost:9876/ntuaflix_api/searchtitle'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers, json={"titlePart": titlepart})
    if args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print(response.json())

#name
if args.scope == 'name':
    nameid = args.nameid
    url = f'http://localhost:9876/ntuaflix_api/name/{nameid}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers, json={"nameid": nameid})
    if args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print(response.json())


#searchname
if args.scope == 'searchname':
    name = str(args.name)
    url = f'http://localhost:9876/ntuaflix_api/searchname'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers, json={"name": name})
    if args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print(response.json())

#bygenre
if args.scope == 'bygenre':
    genre = str(args.genre)
    minrating = args.min
    url = f'http://localhost:9876/ntuaflix_api/bygenre'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers, json={"qgenre": genre, "minrating": minrating})
    if args.format == 'csv':
        df = pd.json_normalize(response.json())
        df.to_csv()
        print(df)
    else:
        print(response.json())


