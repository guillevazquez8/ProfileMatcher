# Guille's Profile Matcher

Welcome to Guille's Porfile Matcher! A matcher for video games between the player and available campaigns. 

## API setup
It runs with Python 3.12. Create a venv, install requirements.txt, and configure your database user, password, and database name in the config file in `config/config.py`.

## How to run it
To start the API, just write `flask --app run run` in the terminal from inside the project. 

I've prepared some documentation to interact with the API, you can find it in `localhost:5000/apidocs`.

I've also included some tests that you can use to check that everything is working as it should.

## Endpoints

- `/get_client_config/<string:player_id>`: it updates the player with all running campaigns where the player suits its matchers. I get the running campaigns with the endpoint `/campaign/enabled`, which returns all campaigns with enabled=true.
  
- `/init_data`: it initializes a player and a campaign with just sending an empty POST, in order to have some data in the database before testing the first endpoint.

- CRUD endpoints for Player and Campaign.

## Some details regarding the API's functioning

- The code is organized in two folders, Player and Campaign, each with their model, schema, db, and routes layers. I've done this for the sake of simplicity, even though every table could have their own set of layers.

- Data entry validation is done with pydantic.

- There is a class UTCDatetime in `app/helpers.py` which saves all datetimes introduced in the database in UTC, and returns them in the same way ending in "Z" to indicate zero timezone, as I've noticed the data of the task was written in this format.

- All endpoints include docstrings in yaml format under them for documentation purposes.
  
