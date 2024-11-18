# Guille's Profile Matcher

This is a profile matcher for video games. 

## API Configuration
It runs with Python 3.12. Create a venv, install requirements.txt, and configure your database user, password, and database name in the config file in `config/config.py`.

## How to run it
To start the API, just write `flask --app run run` in the terminal from inside the project. 

I've prepared some documentation to interact with the API, you can find it in `localhost:5000/apidocs`.

I've also included some tests that you can use to check that everything is working as it should.

## Endpoints
I've included CRUD endpoints for Player and Campaign, apart from the key endpoint of the task: `/get_client_config/<string:player_id>`

But before trying this endpoint you need to have some data in the database. I've made the endpoint `/init_data` to initialize a player and a campaign with just sending an empty POST.

After that, by calling the endpoint `/get_client_config/{player_id}`, it updates the player with all running campaigns where the player suits its matchers. 
I get the running campaigns with the endpoint `/campaign/enabled`, which returns all campaigns with enabled=true.


## Some details regarding the API's functioning

I've organized the code in just two folders, Player and Campaign. I've done this for the sake of simplycity, even though every table could have their own folder.

I've included data entry validation with pydantic.

I've included a class UTCDatetime in `app/helpers.py` which saves all datetimes introduced in the database in UTC, and returns them in the same way ending in "Z" to indicate zero timezone, as I've noticed the data of the task was being written like this.
  
