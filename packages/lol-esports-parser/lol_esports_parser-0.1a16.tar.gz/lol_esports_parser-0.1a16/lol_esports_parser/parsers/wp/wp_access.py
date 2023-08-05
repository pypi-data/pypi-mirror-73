import requests
from retry import retry
from bs4 import BeautifulSoup

from lol_esports_parser.config import endpoints, MAX_RETRIES, RETRY_DELAY
from lol_esports_parser.dto.series_dto import LolSeries, create_series
from lol_esports_parser.dto.wp_dto import LolWpGame
from lol_esports_parser.parsers.wp.wp_parser import parse_wp_game


def get_wp_series(series_url: str, patch: str = None, add_names=True, discrete_mode=True) -> LolSeries:
    """Gets a wp series from its url.

    Args:
        series_url: the URL to the wp match history
        patch: MM.mm patch, to add it to the object as it’s wrong by default in wp
        add_names: whether or not to add names to items, runes, and so on and so forth
        discrete_mode: whether or not to add fields that are specific to this data source
    """
    page = requests.get(series_url)

    soup = BeautifulSoup(page.content, "html.parser")

    games = []
    for link in soup.findAll("a", attrs={"data-matchid": True}):
        games.append(get_wp_game(int(link["data-matchid"]), patch, add_names, discrete_mode))

    return create_series(games)


@retry(tries=MAX_RETRIES, delay=RETRY_DELAY)
def get_wp_game(wp_match_id: int, patch: str = None, add_names=True, discrete_mode=True) -> LolWpGame:
    """Gets a wp game from its match ID.

    Args:
        wp_match_id: the wp match id
        patch: MM.mm patch, to add it to the object as it’s wrong by default in wp
        add_names: whether or not to add names to items, runes, and so on and so forth
        discrete_mode: whether or not to add fields that are specific to this data source
    """

    url = endpoints["wp"]["match_detail"]
    headers = endpoints["wp"]["headers"]

    raw_game = requests.get(f"{url}{wp_match_id}", headers=headers).json()

    return parse_wp_game(raw_game, patch, add_names, discrete_mode)
