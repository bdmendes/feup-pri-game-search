#!/bin/sh
DIR=$(dirname "$0")

cp "$DIR/../data/processed.json" "$DIR/data/processed.json"

docker build $DIR -t steam_games
docker run -it -p 8983:8983 steam_games