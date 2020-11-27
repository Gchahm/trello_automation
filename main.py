import util
import trello_api
import flight_checker

if __name__ == '__main__':
    trello_cards = trello_api.get_cards()
    util.save_json_to_file(trello_cards, 'trello_cards.json')
    flights, errors = flight_checker.check_flights(trello_cards)
    util.save_json_to_file(flights, 'flight_details.json')
    util.save_json_to_file(errors, 'errors.json')
