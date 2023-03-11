# this server needs:

## postgres database
###### with tables: 
###### token (username text primary key, token uuid)
###### students (id integer generated always as identity not null primary key, fname text not null, lname text not null, sname text, group_ text not null, age int)

## .env file with credentials:
###### postgres: PG_DBNAME, PG_HOST, PG_PORT, PG_USER, PG_PASSWORD
###### yandex weather api: YANDEX_KEY
