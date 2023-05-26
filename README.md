# Rapid Crawler

The goal of the service is to parse web-sites and save the latest posts to a database with a certain metadata (title, date, user, content)

## Requirements
* Python 3.11
* Poetry 1.4.2

## Run it

The repo contains Dockerfile and docker-compose setup for multiplatform local run.

```bash
cd path/to/project/rapid-crawler
docker-compose up -d
```
In order to list all the running containers
```bash
docker ps
```
Show the log of the service
```bash
docker logs -f rapid-crawler
```
To run the service locally without docker-compose make sure you have running mongoDB instance on your machine
```bash
cd path/to/project/rapid-crawler
poetry install
poetry run python main.py
```

## Settings and ENVs

| ENV      | Description | Default |
| ---------------- | ------------- | ------------- |
| DB_CONN_STR   | connection string to MongoDB | mongodb://localhost:27017/ |
| SCHEDUALER_INTERVAL_SEC  | set number of seconds between scrawling updates | 120 |
| PARSING_URLS   | define urls to parse with coma separator | https://pastebin.com/archive |
| NUM_OF_PROCESSES  | number of processes for parallel parser processing | 1 |

If you define a few urls to parse then make sure you have added a new parser class to parsers folder and updated a PARSER_MAP in the  factory in order to support a new structure of added resourse.

Also consider encreasing number of processes in case of adding a new sites for parsing.

## How it works

New processes with workers are created once the programm is started. Workers are waiting for a new items to process in the queue. 

Main thread runs a schedualer with set interval (default 120s). On every single iteration schedualer adds a new command classes to the queue for handling. Factory defines which class will handle the parcing depending on the given url.

Once the worker received a new item it runs the parser. First it collects all the urls of the posts. Then it parses all the pages of the posts to receive needed metadata utilising multithreading. 

When all the metadata is collected the programm writes each post to the database. All the next parcing sessions check the latest post in the database and handles only the newest posts since the last time in order to prevent redundant processing time.

## Unit tests and linter
In order to run unit tests
```bash
cd path/to/project/rapid-crawler
poetry install
poetry run pytest
poetry run black .
poetry run flake8
```