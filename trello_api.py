from datetime import datetime
from json.decoder import JSONDecodeError

import requests
import json
import util


class TrelloHelper:

    def __init__(self, board_id='Uu80gVQa'):
        self.trello_api = TrelloAPI(board_id)
        self.list_ids = [item['id'] for item in self.trello_api.get_lists() if item['name'] in ['Ida', 'Volta']]
        labels = [TrelloLabel(label) for label in self.trello_api.get_board_labels()]
        self.warn_label = [label for label in labels if label.color == 'purple'].pop()
        self.error_label = [label for label in labels if label.color == 'orange'].pop()

    def get_cards(self):
        return [TrelloCard(item) for item in self.trello_api.get_cards() if item['idList'] in self.list_ids]

    def get_comments(self, card_id, identifier='Bot'):
        """
        Get all comment actions of a specific card
        :param card_id: the card id of the card to be looked at
        :param identifier: only comments that contain the intentifier in it's text will be returned
        :return: A list of all comments sorted by date order
        """
        comments = [TrelloComment(x) for x in self.trello_api.get_card_comments(card_id)]
        bot_comments = [x for x in comments if x.text.count(identifier) > 0]
        bot_comments.sort()
        return bot_comments

    def add_comment(self, card_id, text):
        response = self.trello_api.add_comment(card_id, text)
        return TrelloComment(response)

    def update_comment(self, card_id, comment_id, text):
        result = self.trello_api.update_comment(card_id, comment_id, text)
        return TrelloComment(result)

    def delete_comment(self, card_id, comment_id):
        return self.trello_api.delete_comment(card_id, comment_id)

    def add_warn_label(self, card_id):
        return self.trello_api.add_label(card_id, self.warn_label.label_id)

    def add_error_label(self, card_id):
        return self.trello_api.add_label(card_id, self.error_label.label_id)

    def remove_warn_label(self, card_id):
        return self.trello_api.remove_label(card_id, self.warn_label.label_id)

    def remove_error_label(self, card_id):
        return self.trello_api.remove_label(card_id, self.error_label.label_id)

class TrelloAPI:

    def __init__(self, board_id):
        self._board_id = board_id

        self._base_headers = {
            "Accept": "application/json"
        }
        self._base_params = {
            'key': util.get_env_variable('TRELLO_KEY'),
            'token': util.get_env_variable('TRELLO_TOKEN')
        }

    def get_lists(self):
        url = f'https://api.trello.com/1/boards/{self._board_id}/lists'
        return self._trello_base_request(url)

    def get_cards(self):
        """
        Loads all cards in the board from trello
        :return: List of all cards with the links of tap.py tracker
        """
        board_cards_url = f'https://api.trello.com/1/boards/{self._board_id}/cards'
        return self._trello_base_request(board_cards_url)

    def get_card_comments(self, card_id):
        url = f'https://api.trello.com/1/cards/{card_id}/actions'
        actions = self._trello_base_request(url)
        return [x for x in actions if x['type'] == 'commentCard']

    def add_comment(self, card_id, comment):
        url = f"https://api.trello.com/1/cards/{card_id}/actions/comments"
        params = {'text': comment}
        return self._trello_base_request(url, 'POST', params=params)

    def update_comment(self, card_id, comment_id, text):
        url = f'https://api.trello.com/1/cards/{card_id}/actions/{comment_id}/comments'
        return self._trello_base_request(url, action='PUT', params={'text': text})

    def delete_comment(self, card_id, comment_id):
        url = f'https://api.trello.com/1/cards/{card_id}/actions/{comment_id}/comments'
        return self._trello_base_request(url, 'DELETE')

    def get_board_labels(self):
        url = f'https://api.trello.com/1/boards/{self._board_id}/labels'
        return self._trello_base_request(url)

    def add_label(self, card_id, label_id):
        url = f'https://api.trello.com/1/cards/{card_id}/idLabels'
        return self._trello_base_request(url, 'POST', params={'value': label_id})

    def remove_label(self, card_id, label_id):
        url = f'https://api.trello.com/1/cards/{card_id}/idLabels/{label_id}'
        return self._trello_base_request(url, 'DELETE')

    def _trello_base_request(self, url, action='GET', headers=None, params=None):
        if params is None:
            params = {}
        if headers is None:
            headers = {}

        headers = {**self._base_headers, **headers}
        params = {**self._base_params, **params}
        response = requests.request(
            action,
            url,
            headers=headers,
            params=params,
        )
        try:
            return json.loads(response.text)
        except JSONDecodeError:
            return {'error': response.text}

class TrelloCard:

    def __init__(self, raw):
        self.raw = raw
        self.card_id = raw['id']
        self.tap_url = raw['desc'].replace('\n', '')
        self.name = raw['name']


class TrelloComment:

    def __init__(self, raw):
        self.raw = raw
        self.comment_id = raw['id']
        self.created_at = datetime.fromisoformat(raw['date'][:16])
        self.data = raw['data']
        self.text = self.data['text']
        self.card = self.data['card']
        self.card_id = self.card['id']

    def __repr__(self):
        return f'Comment {self.comment_id}: card {self.card_id}'

    def __lt__(self, other):
        return self.created_at < other.created_at

    def __eq__(self, other):
        return self.text.replace('#', '') == other.text.replace('#', '')


class TrelloLabel:

    def __init__(self, raw):
        self.raw = raw
        self.label_id = raw['id']
        self.color = raw['color']


def tests():
    helper = TrelloHelper('yLKe88Cg')
    assert isinstance(helper.warn_label, TrelloLabel)
    assert len(helper.list_ids) == 2
    test_card_id = 'm7uj33Cv'
    trello_cards = helper.get_cards()
    for card in trello_cards:
        assert isinstance(card, TrelloCard)
    comments = helper.get_comments(test_card_id)
    for comment in comments:
        assert isinstance(comment, TrelloComment)
    comment = helper.add_comment(test_card_id, 'text')
    assert isinstance(comment, TrelloComment)
    assert comment.text == 'text'
    updated = helper.update_comment(comment.card_id, comment.comment_id, 'new text')
    assert isinstance(updated, TrelloComment)
    assert updated.text == 'new text'
    assert not comment == updated
    updated.text = 'text'
    assert comment == updated
    deleted = helper.delete_comment(updated.card_id, updated.comment_id)
    assert isinstance(deleted, dict)
    assert deleted['_value'] is None
    print('tests passed!')
    warn_label = helper.add_warn_label(updated.card_id)

    error_label = helper.add_error_label(updated.card_id)


if __name__ == '__main__':
    tests()
