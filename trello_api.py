import requests
import json
import util
import logging

BOARD_ID = 'Uu80gVQa'


def get_filtered_cards():
    list_ids = [item['id'] for item in get_lists() if item['name'] in ['Ida', 'Volta']]
    cards = [item for item in get_cards() if item['idList'] in list_ids]
    return _parse_result(cards)


def get_cards():
    """
    Loads all cards in the board from trello
    :return: List of all cards with the links of tap.py tracker
    """
    # Loads cards from trello board
    board_cards_url = f'https://api.trello.com/1/boards/{BOARD_ID}/cards'
    response = _trello_base_request(board_cards_url)
    logging.info('cards loaded')
    return json.loads(response.text)


def add_comment(card_id, comment):
    url = f"https://api.trello.com/1/cards/{card_id}/actions/comments"
    params = {'text': comment}
    request = _trello_base_request(url, 'POST', params=params)
    logging.info('comment added: ' + card_id)
    return request


def get_lists():
    url = f'https://api.trello.com/1/boards/{BOARD_ID}/lists'
    response = _trello_base_request(url)
    return json.loads(response.text)


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
    :return: list of objects that contain the id of each card and the tap.py tracker link attached to the card
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
