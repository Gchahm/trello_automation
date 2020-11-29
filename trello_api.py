from datetime import datetime
import requests
import json
import util


class TrelloHelper:

    def __init__(self, board_id='Uu80gVQa'):
        self.trello_api = TrelloAPI(board_id)
        self.list_ids = [item['id'] for item in self.trello_api.get_lists() if item['name'] in ['Ida', 'Volta']]
        labels = [TrelloLabel(label) for label in self.trello_api.get_board_labels()]
        self.warn_label = [label for label in labels if label.color == 'purple'].pop()

    def get_filtered_cards(self):
        return [Card(item) for item in self.trello_api.get_cards() if item['idList'] in self.list_ids]

    def add_comment(self, card_id, text):
        return self.trello_api.add_comment(card_id, text)

    def delete_comment(self, card_id, comment_id):
        return self.trello_api.delete_comment(card_id, comment_id)

    def get_comments(self, card_id, identifier='Flight Number'):
        """
        Get all comment actions of a specific card
        :param card_id: the card id of the card to be looked at
        :param identifier: only comments that contain the intentifier in it's text will be returned
        :return: A list of all comments sorted by date order
        """
        actions = self.trello_api.get_card_actions(card_id)
        comments = [Comment(x) for x in actions if x['type'] == 'commentCard']
        bot_comments = [x for x in comments if x.text.count(identifier) > 0]
        bot_comments.sort()
        return bot_comments

    def get_last_comment(self, card_id):
        comments = self.get_comments(card_id)
        return comments.pop() if comments else None

    def update_comments(self, card_id, comment_id, text):
        result = self.trello_api.update_comment(card_id, comment_id, text)
        return result

    def add_warn_label(self, card_id):
        return self.trello_api.add_label(card_id, self.warn_label.label_id)


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

    def add_label(self, card_id, label_id):
        url = f'https://api.trello.com/1/cards/{card_id}/idLabels'
        return self._trello_base_request(url, 'POST', params={'value': label_id})

    def get_board_labels(self):
        url = f'https://api.trello.com/1/boards/{self._board_id}/labels'
        response = self._trello_base_request(url)
        return json.loads(response.text)

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
            params=params,
        )

    def delete_comment(self, card_id, comment_id):
        url = f'https://api.trello.com/1/cards/{card_id}/actions/{comment_id}/comments'
        return self._trello_base_request(url, 'DELETE')


class Card:

    def __init__(self, raw):
        self.raw = raw
        self.card_id = raw['id']
        self.tap_url = raw['desc'].replace('\n', '')


class Comment:

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

    def compare_comment(self, comment):
        """
        Compare a text with the current comment
        :param comment: comment text for the nex comment
        :return: True / false if they are equal
        """
        return self.text.replace('#', '') == comment.replace('#', '')


class TrelloLabel:

    def __init__(self, raw):
        self.raw = raw
        self.label_id = raw['id']
        self.color = raw['color']


if __name__ == '__main__':
    helper = TrelloHelper()
    for card in helper.get_filtered_cards():
        comments = helper.get_comments(card.card_id)
        if len(comments) > 1:
            comment = comments[0]
            deleted = helper.delete_comment(comment.card_id, comment.comment_id)
