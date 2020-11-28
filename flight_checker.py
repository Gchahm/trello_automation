import scraper


def check_flights(parsed):
    for item in parsed:
        url = item['tap_url']
        item_id = item['id']
        try:
            result = {
                'id': item_id,
                'url': url,
                'flight_details': scraper.get_flight_details(url, max_wait=20)
            }
            yield result, None
        except Exception as err:
            yield None, {'id': item_id, 'message': str(err)}

