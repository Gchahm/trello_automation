import requests
import json
import util


def get_cards():
    """
    Loads all cards in the board from trello
    :return: List of all cards with the links of tap tracker
    """
    # Loads cards from trello board
    board_cards_url = "https://api.trello.com/1/boards/yLKe88Cg/cards"
    response = _trello_get(board_cards_url)
    cards = json.loads(response.text)
    return _parse_result(cards)


def _trello_get(url, headers=None, params=None):
    if params is None:
        params = {}
    if headers is None:
        headers = {}

    headers = {**_BASE_HEADERS, **headers}
    params = {**__BASE_PARAMS, **params}
    return requests.request(
        "GET",
        url,
        headers=headers,
        params=params
    )


_BASE_HEADERS = {
    "Accept": "application/json"
}


__BASE_PARAMS = {
    'key': util.get_env_variable('TRELLO_KEY'),
    'token': util.get_env_variable('TRELLO_TOKEN')
}


def _parse_result(cards):
    """
    :param cards: json result from trello cards
    :return: list of objects that contain the id of each card and the tap tracker link attached to the card
    """
    result = []
    for card in cards:
        parsed = {
            'id': card['id'],
            'tap_url': card['desc'].replace('\n', '')
        }
        result.append(parsed)
    return result


if __name__ == '__main__':
    get_cards()
