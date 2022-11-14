#!/bin/sh
DIR=$(dirname "$0")

cp "$DIR/../data/processed.json" "$DIR/data/processed.json"

# Start Solr
docker stop steam_games
docker rm steam_games
docker run -d --name=steam_games -p 8983:8983 solr:8.10

# Wait for Solr to start
sleep 3

# Delete the core to prevent indexing of the same data multiple times
docker exec steam_games bin/solr delete -c steam-games

# Create the core
docker exec steam_games bin/solr create_core -c steam-games

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @$DIR/data/schema.json \
    http://localhost:8983/solr/steam-games/schema

# Populate collection via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @$DIR/data/processed.json \
    http://localhost:8983/solr/steam-games/update?commit=true

echo "Solr is running on http://localhost:8983/solr/#/steam-games/core-overview"
echo "You can kill this container at anytime with 'docker stop steam_games'"