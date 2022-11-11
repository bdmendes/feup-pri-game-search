#!/bin/bash

# Start Solr in background mode so we can use the API to upload the schema
solr start

bin/solr create_core -c steam-games

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/schema.json \
    http://localhost:8983/solr/steam-games/schema

# Populate collection
bin/post -c steam-games /data/steam-games.json

# Restart in foreground mode so we can access the interface
solr restart -f
