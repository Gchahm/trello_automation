import requests
import json
import util
import logging


class TrelloHelper:

    def __init__(self, board_id='Uu80gVQa'):
        self.trello_api = TrelloAPI(board_id)

    def get_filtered_cards(self):
        list_ids = [item['id'] for item in self.trello_api.get_lists() if item['name'] in ['Ida', 'Volta']]
        return [Card(item) for item in self.trello_api.get_cards() if item['idList'] in list_ids]

    def add_comment(self, card_id, comment):
        return self.trello_api.add_comment(card_id, comment)

    def get_comments(self, card_id):
        actions = self.trello_api.get_card_actions(card_id)
        comments = [Comment(x) for x in actions if x['type'] == 'commentCard']
        bot_comments = [x for x in comments if x.text.count('Flight Number') > 0]
        return bot_comments

    def update_comments(self, card_id, comment_id, text):
        result = self.trello_api.update_comment(card_id, comment_id, text)
        return result


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

    def get_cards(self):
        """
        Loads all cards in the board from trello
        :return: List of all cards with the links of tap.py tracker
        """
        board_cards_url = f'https://api.trello.com/1/boards/{self._board_id}/cards'
        response = self._trello_base_request(board_cards_url)
        return json.loads(response.text)

    def get_lists(self):
        url = f'https://api.trello.com/1/boards/{self._board_id}/lists'
        response = self._trello_base_request(url)
        return json.loads(response.text)

    def get_card_actions(self, card_id):
        url = f'https://api.trello.com/1/cards/{card_id}/actions'
        response = self._trello_base_request(url)
        return json.loads(response.text)

    def add_comment(self, card_id, comment):
        url = f"https://api.trello.com/1/cards/{card_id}/actions/comments"
        params = {'text': comment}
        request = self._trello_base_request(url, 'POST', params=params)
        return request

    def update_comment(self, card_id, comment_id, text):
        url = f'https://api.trello.com/1/cards/{card_id}/actions/{comment_id}/comments'
        response = self._trello_base_request(url, action='PUT', params={'text': text})
        return response

    def _trello_base_request(self, url, action='GET', headers=None, params=None):
        if params is None:
            params = {}
        if headers is None:
            headers = {}

        headers = {**self._base_headers, **headers}
        params = {**self._base_params, **params}
        return requests.request(
            action,
            url,
            headers=headers,
            params=params
        )


class Card:

    def __init__(self, raw):
        self.raw = raw
        self.card_id = raw['id']
        self.tap_url = raw['desc'].replace('\n', '')


class Comment:

    def __init__(self, raw):
        self.raw = raw
        self.comment_id = raw['id']
        self.data = raw['data']
        self.text = self.data['text']
        self.card = self.data['card']
        self.card_id = self.card['id']

    def __repr__(self):
        return f'Comment {self.comment_id}: card {self.card_id} {self.text}'


def update_comments(comments):
    for comment in comments:
        text = comment['text'].replace('#', '##')


if __name__ == '__main__':
    helper = TrelloHelper()
    for card in helper.get_filtered_cards():
        for comment in helper.get_comments(card.card_id):
            updated = helper.update_comments(comment.card_id, comment.comment_id, comment.text.replace('#', '##'))
