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
    response = _trello_base_request(board_cards_url)
    cards = json.loads(response.text)
    return _parse_result(cards)


def add_comment(card_id, comment):
    url = f"https://api.trello.com/1/cards/{card_id}/actions/comments"
    params = {'text': comment}
    return _trello_base_request(url, 'POST', params=params)


def _trello_base_request(url, request_type='GET', headers=None, params=None):
    if params is None:
        params = {}
    if headers is None:
        headers = {}

    headers = {**_BASE_HEADERS, **headers}
    params = {**_BASE_PARAMS, **params}
    return requests.request(
        request_type,
        url,
        headers=headers,
        params=params
    )


_BASE_HEADERS = {
    "Accept": "application/json"
}


_BASE_PARAMS = {
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
