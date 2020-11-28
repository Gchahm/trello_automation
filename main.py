import logging
import file_manager
import trello_api
import scraper


def automation(trello_cards):
    tap_scrapper = scraper.TapScrapper(max_wait=20)
    for card in trello_cards:
        card_id = card['id']
        try:
            # Get reservation details from TAP Website
            reservation_details = tap_scrapper.get_reservation_details(card['tap_url'])
            # Add comment to Card based on the reservation
            add_comment(card_id, reservation_details)
            # Save reservation details to file
            file_manager.add_flight({**card, 'reservation_details': reservation_details})
        except Exception as err:
            # Log Error to Log file and save to error file
            logging.error('error: ' + card_id + str(err))
            file_manager.add_error({**card, 'message': str(err)})
    logging.debug('finished')


def load_trello_cards():
    trello_cards = trello_api.get_filtered_cards()
    file_manager.save_cards(trello_cards)
    return trello_cards


def add_comment(card_id, reservation_details):
    comment = ''
    for fd in reservation_details:
        for key, value in fd.items():
            comment += f'{key}: {value}\n'
        comment += '\n'
    trello_api.add_comment(card_id, comment)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    # cards = file_manager.get_errors()
    cards = load_trello_cards()
    automation(cards)
