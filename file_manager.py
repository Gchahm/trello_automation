import util


def get_errors():
    try:
        errors = util.load_json_from_file('errors.json')
        return errors
    except FileNotFoundError:
        return []


def add_error(error):
    errors = get_errors()
    errors.append(error)
    util.save_json_to_file(errors, 'errors.json')


def get_flights():
    try:
        flights = util.load_json_from_file('flight_details.json')
        return flights
    except FileNotFoundError:
        return []


def add_flight(flight):
    flights = get_flights()
    flights.append(flight)
    util.save_json_to_file(flights, 'flight_details.json')


def save_cards(cards):
    util.save_json_to_file(cards, 'trello_cards.json')


