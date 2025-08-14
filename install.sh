#!/bin/bash


# Install Flask for web application development
pip install Flask

pip install flask-login
# Install PyMongo to interact with MongoDB
pip install pymongo

# Install Flask-JWT-Extended for handling JWTs in Flask applications
pip install Flask-JWT-Extended

# Install Werkzeug for utilities in handling security (passwords) and exceptions
pip install Werkzeug

pip install pandas

cd ./front-end

npm install

cd ../testing

npm install newman

echo "All necessary packages have been installed."


# Specify the folder containing JSON files
FOLDER="./data/dbdump"

# Loop through each JSON file in the folder and import it into MongoDB
for file in $FOLDER/*.json; do
    # Extract the base name of the file for collection name
    BASENAME=$(basename "$file" .json)

    # Use the base name as the collection name
    COLLECTION=${BASENAME}

    # Import the file into MongoDB
    echo "Importing $file into collection $COLLECTION"
    mongoimport --db "local" --collection "$COLLECTION" --file "$file" --jsonArray
done

echo "All files have been imported."
