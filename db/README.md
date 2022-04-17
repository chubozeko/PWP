# Database Design

## Dependencies and Tools Used

- MySQL - 8.0.26
- Docker Desktop - 4.7.0
  - Docker Compose - 3.0
- Python MySQL libraries
  - mysql-connector-python - v8.0.28
  - pymysql - v1.0.2
  - cryptography - v36.0.2

## Setting up the MySQL framework and libraries

MySQL can be [**downloaded**](https://dev.mysql.com/downloads/mysql/) and [**installed**](https://dev.mysql.com/doc/mysql-installer/en/) on any machine using the relevant (installer or package), or by installing and connecting to a [**MySQL image**](https://hub.docker.com/_/mysql) on Docker.
In this case, MySQL was installed as a Docker image with Docker Compose using `docker-compose.yml`:
```
version: '3'
services:
  mysql-db:
    container_name: pwp-mysql
    image: mysql
    command: --default-authentication-plugin=mysql_native_password
    environment:
      MYSQL_ROOT_PASSWORD: mysql-password
    restart: always
    ports:
      - "127.0.0.1:3306:3306"

networks:
  default:
    name: pwp
```
(<i><strong>Note:</strong> make sure you change '<i>MYSQL_ROOT_PASSWORD</i>' to a stronger password.</i>)

Once the MySQL Docker image is up and running, we can install each of the following Python libraries that are needed to connect to the database, using ``pip install``:
```commandline
pip install mysql-connector-python
pip install pymysql
pip install cryptography
```

Alternatively, we can install all the required libraries found in the ``requirements.txt`` file with the following command:
```commandline
pip install -r requirements.txt --user
```

## Loading the Database
### 1. Creating the database
Once MySQL has been set up, the database can be created using the ``pwp_db_create.sql`` file. This query can be run on the MySQL platform to create the tables. 
Each database entity has a subdirectory containing an SQL query that creates their table.
### 2. Populating the database
Once the MySQL database has been created, the database can be populated with some default data using the ``pwp_db_insert.sql`` file. This query can be run on the MySQL platform to populate the tables.
Each database entity has a subdirectory containing an SQL query that inserts data into their tables.

### Alternative Method: Create + Populate database
You can run ``load_database.py`` from the ``db`` directory, which loads the database by creating and populating the database. 
This file loads the database using the database credentials defined in ``credentials.json`` which would be found in the ``db`` directory (Note: ``credentials.json`` is currently hidden in this repository for privacy reasons).
```commandline
python load_database.py
```
