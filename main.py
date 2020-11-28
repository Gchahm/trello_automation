import util
import trello_api
import flight_checker


def automation():
    trello_cards = load_cards()
    for flight in get_flight_details(trello_cards):
        add_comment(flight)


def load_cards():
    trello_cards = trello_api.get_cards()
    util.save_json_to_file(trello_cards, 'trello_cards.json')
    return trello_cards


def get_flight_details(trello_cards):
    flights = []
    errors = []
    for flight, error in flight_checker.check_flights(trello_cards):
        if flight is not None:
            flights.append(flight)
            util.save_json_to_file(flights, 'flight_details.json')
            yield flight
        if error is not None:
            errors.append(error)
            util.save_json_to_file(errors, 'errors.json')


def add_comment(flight):
    flight_details = flight['flight_details']
    comment = ''
    for fd in flight_details:
        for key, value in fd.items():
            comment += f'{key}: {value}\n'
        comment += '\n'
    trello_api.add_comment(flight['id'], comment)


if __name__ == '__main__':
    automation()
