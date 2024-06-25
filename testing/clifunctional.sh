#! /bin/bash

echo "Login as admin"
python3 ../cli-client/cli.py se2339 login --username admin --passw admin
echo -e "\n"

echo "Perform a healtcheck"
python3 ../cli-client/cli.py se2339 healthcheck
echo -e "\n"

echo "Get the user info with seen movie IDs"
python3 ../cli-client/cli.py se2339 user --username jim 
echo -e "\n"

echo "Upload a new name document"
python3 ../cli-client/cli.py se2339 newnames --filename ../data/csvdata/truncated_name.basics.tsv
echo -e "\n"

echo "Upload a new title document"
python3 ../cli-client/cli.py se2339 newtitles --filename ../data/csvdata/truncated_title.basics.tsv
echo -e "\n"

echo "Logout"
python3 ../cli-client/cli.py se2339 logout
echo -e "\n"

echo "Login as a user"
python3 ../cli-client/cli.py se2339 login --username jim --passw 1000
echo -e "\n"

echo "Get titles that have the word 'star' in their title"
python3 ../cli-client/cli.py se2339 searchtitle --titlepart star 
echo -e "\n"

echo "Get info about movie with ID tt0000929"
python3 ../cli-client/cli.py se2339 title --titleID tt0000929 
echo -e "\n"

echo "Get info about movie with ID tt0000977"
python3 ../cli-client/cli.py se2339 title --titleID tt0000977
echo -e "\n"

echo "Get titles that have genre 'comedy' and minumum rating 7"
python3 ../cli-client/cli.py se2339 bygenre --genre Comedy --min 7 
echo -e "\n"

echo "Get titles that have genre 'action' and minumum rating 8"
python3 ../cli-client/cli.py se2339 bygenre --genre Action --min 7 
echo -e "\n"


echo "Get objects about names that have name 'Tom'"
python3 ../cli-client/cli.py se2339 searchname --name Tom 
echo -e "\n"

echo "Logout" 
python3 ../cli-client/cli.py se2339 logout
echo -e "\n"

echo "Login as admin"
python3 ../cli-client/cli.py se2339 login --username admin --passw admin
echo -e "\n"

echo "Change the password of user jim"
python3 ../cli-client/cli.py se2339 adduser --username jim --passw 1001
echo -e "\n"

echo "Reset database"
python3 ../cli-client/cli.py se2339 resetall
echo -e "\n"

echo "Logout" 
python3 ../cli-client/cli.py se2339 logout
echo -e "\n"
