import scraper


def check_flights(parsed):
    flights = []
    errors = []
    for item in parsed[:10]:
        url = item['tap_url']
        item_id = item['id']
        try:
            flight_details = scraper.get_flight_details(url, max_wait=20)
            flights.append({
                'id': item_id,
                'url': url,
                'flight_details': flight_details
            })
        except:
            errors.append(item_id)

    return flights, errors
