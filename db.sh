#!/bin/bash

# Specify the MongoDB database
DATABASE="local"

# Specify the folder containing JSON files
FOLDER="./data/dbdump"

# Initiate the database by creating and then dropping a dummy collection
echo "Initiating $DATABASE database..."
mongo $DATABASE --eval "db.createCollection('init_collection'); db.init_collection.drop();"
echo "Database $DATABASE initiated."

# Loop through each JSON file in the folder and import it into MongoDB
for file in $FOLDER/*.json; do
    # Extract the base name of the file for collection name
    BASENAME=$(basename "$file" .json)

    # Use the base name as the collection name
    COLLECTION=${BASENAME}

    # Import the file into MongoDB
    echo "Importing $file into collection $COLLECTION"
    mongoimport --db $DATABASE --collection "$COLLECTION" --file "$file" --jsonArray
done

echo "All files have been imported."

