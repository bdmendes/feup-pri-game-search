#!/bin/sh

# Start Solr in background mode so we can use the API to upload the schema
bin/solr start

bin/solr delete -c steam-games

bin/solr create_core -c steam-games

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/schema.json \
    http://localhost:8983/solr/steam-games/schema

# Populate collection via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/processed.json \
    http://localhost:8983/solr/steam-games/update?commit=true

# Restart in foreground mode so we can access the interface
bin/solr restart -f
