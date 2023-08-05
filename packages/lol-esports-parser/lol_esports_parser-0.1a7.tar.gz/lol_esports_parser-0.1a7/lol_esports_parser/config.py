import json
import os

# Configuration for endpoints retries
TRIES = os.environ.get("LOL_ESPORTS_PARSER_RETRIES") or 2
DELAY = os.environ.get("LOL_ESPORTS_PARSER_DELAY") or 10  # Time to sleep on errors (in seconds)

# Required for pro endpoints
riot_username = os.environ["RIOT_USERNAME"]
riot_password = os.environ["RIOT_PASSWORD"]

# Required for amateur games played on live servers
api_key = os.environ.get("RIOT_API_KEY")

# Local configuration files
config_folder = os.path.join(os.path.expanduser("~"), ".config", "lol_esports_parser")
endpoints_location = os.path.join(config_folder, "endpoints.json")

if not os.path.exists(config_folder):
    os.makedirs(config_folder)
    raise FileNotFoundError(f"Please create {endpoints_location}.")

with open(endpoints_location) as file:
    endpoints = json.load(file)
