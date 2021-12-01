docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)

docker build -t text_and_translate .
docker run -dp 3000:3000 --name text_and_translate text_and_translate