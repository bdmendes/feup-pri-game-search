#!/bin/sh
DIR=$(dirname "$0")

cp "$DIR/../data/processed.json" "$DIR/data/processed.json"

# Kill any existing solr instance
echo "Killing any existing solr docker instance"
docker stop solr_steam
docker rm solr_steam

# Start Solr
echo ""
echo "Starting Solr Docker container"
docker run -d --name=solr_steam -p 8983:8983 solr:8.10

# Wait for Solr to start
sleep 2

# Delete the core to prevent indexing of the same data multiple times
echo ""
echo "Deleting old cores"
docker exec solr_steam bin/solr delete -c games_simple
docker exec solr_steam bin/solr delete -c games_tuned

# Create the simple and tuned cores
echo ""
echo "Creating new core"
docker exec solr_steam bin/solr create_core -c games_simple
docker exec solr_steam bin/solr create_core -c games_tuned

# Schema definition via API
echo ""
echo "Setting up schema"
curl -X POST -H 'Content-type:application/json' \
    --data-binary @$DIR/data/schema.json \
    http://localhost:8983/solr/games_tuned/schema

# Populate collection via API
echo ""
echo "Indexing data"
curl -X POST -H 'Content-type:application/json' \
    --data-binary @$DIR/data/processed.json \
    http://localhost:8983/solr/games_simple/update?commit=true
curl -X POST -H 'Content-type:application/json' \
    --data-binary @$DIR/data/processed.json \
    http://localhost:8983/solr/games_tuned/update?commit=true

echo ""
echo "Solr is running on http://localhost:8983/solr/#/games_tuned/core-overview"
echo "You can kill this container anytime with 'docker stop solr_steam'"