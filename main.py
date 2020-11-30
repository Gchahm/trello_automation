import logging
from datetime import datetime
import file_manager
import trello_api
import scraper


class Automation:

    def __init__(self, board_id='Uu80gVQa'):
        self.trello_helper = trello_api.TrelloHelper(board_id)
        self.tap_scrapper = scraper.TapScrapper(max_wait=60)
        self.trello_cards = None

    def start(self):
        self.load_trello_cards()
        self.update_loaded_cards()

    def update_loaded_cards(self):
        for card in self.trello_cards:
            try:
                # Get reservation details from TAP Website and save in files
                print('Get details from TAP for', card.card_name)
                reservation_details = self.get_reservation_details(card)
                self.update_trello_card(card, reservation_details)
            except Exception as err:
                # Log Error to Log file and save to error file
                logging.error('error: ' + card.card_id + str(err))
                file_manager.add_error({**card.__dict__, 'message': str(err)})

    def get_reservation_details(self, card):
        reservation_details = self.tap_scrapper.get_reservation_details(card.tap_url)
        file_manager.add_flight({**card.__dict__, 'reservation_details': [det.__dict__ for det in reservation_details]})
        return reservation_details

    def load_trello_cards(self):
        print('Loading Trello Cards')
        self.trello_cards = self.trello_helper.get_cards()
        print('Cards Loaded')
        file_manager.save_cards(self.trello_cards)

    def update_trello_card(self, card, reservation_details):
        """
        Get the last comment added by this bot in the card
        Compare the comment with the new comment to be added.
        Add label if mismatch
        Updated the card with a new comment with the details of the flight
        :param card: TrelloCard instance
        :param reservation_details:
        :return:
        """
        print('Get comments from Trello for card', card.name)
        trello_comments = self.trello_helper.get_comments(card.card_id)
        comment_text = '\n'.join(flight.comment() for flight in reservation_details)
        added = self.trello_helper.add_comment(card.card_id, comment_text)

        # Check if the card has comments and if the last comment match with current
        if len(trello_comments) > 0:
            last_comment = trello_comments.pop()
            if last_comment != added:
                print('Adding warning for card', card.name)
                self.trello_helper.add_warn_label(card.card_id)
        # Deletes all the other comments to cap a max of 2 bot comments per card
        for comment in trello_comments:
            print('Deleting extra comment from', card.name)
            self.trello_helper.delete_comment(comment.card_id, comment.comment_id)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename=f"logfiles/log-{datetime.now().timestamp()}", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.debug('Program Started')
    Automation().start()
    logging.debug('Program Finished')
