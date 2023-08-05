import json
import os

# Configuration for endpoints retries
TRIES = os.environ.get('LOL_ESPORTS_PARSER_RETRIES') or 2
DELAY = os.environ.get('LOL_ESPORTS_PARSER_DELAY') or 10  # Time to sleep on errors (in seconds)

# Local configuration files
# TODO REMOVE ALL OF IT AND USE DOTENV?
config_folder = os.path.join(os.path.expanduser("~"), ".config", "lol_esports_parser")
endpoints_location = os.path.join(config_folder, "endpoints.json")
credentials_location = os.path.join(config_folder, "credentials.json")

if not os.path.exists(config_folder):
    os.makedirs(config_folder)
    raise FileNotFoundError(f"Please create {endpoints_location}.")

with open(endpoints_location) as file:
    endpoints = json.load(file)

if not os.path.exists(credentials_location):
    try:
        riot_username = os.environ["RIOT_USERNAME"]
        riot_password = os.environ["RIOT_PASSWORD"]
    except KeyError:
        print(
            f"Creating {credentials_location} locally.\n"
            "This information is required to connect to the ACS endpoints.\n"
            f"Password will be saved in clear, so make sure only your user has read access on the file.\n"
        )
        riot_username = input("Please input your LoL account name:")
        riot_password = input("Please input your LoL account password:")

        with open(credentials_location, "w+") as file:
            json.dump({"account_name": riot_username, "password": riot_password}, file, indent=4)
else:
    with open(credentials_location) as file:
        credentials = json.load(file)
        riot_username = credentials["account_name"]
        riot_password = credentials["password"]
