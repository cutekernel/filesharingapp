FROM mariadb:latest

# ENV MYSQL_ROOT_PASSWORD=password
# COPY employees.sql /docker-entrypoint-initdb.d/

# WORKDIR /all
# COPY data.sql .
# RUN chmod 755 -R /all
EXPOSE 3306
# RUN mysql source /docker-entrypoint-initdb.d/init.sql
WORKDIR /docker-entrypoint-initdb.d/