#!/bin/bash
docker-compose down
docker rmi $(docker images -q)
docker rmi $(docker images -f "dangling=true" -q) -f
docker-compose up -d --build
docker exec -i mariadb mysql -uroot -ppassword filesharingdb < /appdata/data.sql
docker-compose logs -f
