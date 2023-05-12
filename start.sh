#!/bin/bash
docker-compose down
docker rmi app -f
docker rmi mariadb -f
docker rmi $(docker images -f "dangling=true" -q) -f
docker-compose up -d --build
#docker exec -i mariadb mysql -uroot -ppassword filesharingdb < /all/data/data.sql
docker-compose logs -f
