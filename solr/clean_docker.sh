docker kill $(docker container ls -q)
docker rm $(docker container ls -q -a)
docker rmi steam_games