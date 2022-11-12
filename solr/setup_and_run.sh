docker build . -t steam_games
docker run -it -p 8983:8983 steam_games