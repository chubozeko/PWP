# Database Design

## Dependencies and Tools Used
:pencil2: Define database (MySQL, SQLite, MariaDB, MongoDB...) and version; external libraries you might have used

:pencil2: All dependencies (external libraries) and how to install them

- MySQL - (version _)
- Docker - (version _)
- Python MySQL libraries 
  - mysql-connector (version _)
  - mysql-connector-python (version _)
  - mysql-connector-python-rf (version _)
  - pymysql (version _)
  - cryptography (version _)
- _ - (version _)

## Setting up the MySQL framework and libraries
:pencil2: Instructions how to setup the database framework and external libraries you might have used, or a link where it is clearly explained. Include all dependencies (external libraries) and how to install them. Mention the ``requirements.txt`` file.

MySQL can be downloaded and installed on any machine using the relevant (installer or package), or by installing and connecting to a MySQL image on (Docker).
##  Creating the database
Once MySQL has been set up, the database can be created using the ``pwp_db_create.sql`` file. This query can be run on the MySQL platform to create the tables. 
Each database entity has a subdirectory containing an SQL query that creates their table. 
##  Populating the database
