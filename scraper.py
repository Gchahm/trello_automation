from selenium import webdriver
import util
from datetime import datetime


class TapScrapper:

    def __init__(self, max_wait=60):
        driver = util.get_env_variable('DRIVER', 'chrome')
        if driver == 'safari':
            self._driver = webdriver.Safari()
        else:
            self._driver = webdriver.Chrome()
        self._max_wait = max_wait
        self.components = []

    def __del__(self):
        self._driver.close()

    def get_reservation_details(self, url):
        self._driver.get(url)
        self._wait_for_load()
        return self._get_flight_tickets()

    @property
    def driver(self):
        return self._driver

    def _wait_for_load(self):
        for i in range(1, self._max_wait + 1):
            self._driver.implicitly_wait(1)
            components = self._driver.find_elements_by_tag_name('app-extras-flight')
            components_text = [component.text for component in components]
            if len(components_text) > 0 and len(components_text[0]) > 7:
                break
            if i >= self._max_wait:
                raise Exception('waited for to long')

    def _get_flight_tickets(self):
        script = 'return window.sessionStorage["INDRABFMDataStorageService._flight_tickets"]'
        script_result = self._driver.execute_script(script)
        return [Trip(i) for i in util.json.loads(script_result)]


class Trip:

    def __init__(self, raw):
        self.segments = []
        for seg in raw['item']['details']['listSegment']:
            self.segments.append(Segment(seg))

    def comment(self):
        segments = '\n'.join([str(x) for x in self.segments])
        return segments + '\n'


class Segment:

    def __init__(self, raw):
        self.departureAirport = raw['departureAirport']
        self.arrivalAirport = raw['arrivalAirport']
        self.flight = raw['carrier'] + '-' + raw['flightNumber'].zfill(4)
        d1 = datetime.fromisoformat(raw['departureDate'][:-1])
        self.departureDate = d1.strftime(format='%d/%m/%y %H:%M')
        self.flightFlown = raw['flightFlown']
        self.add_status = raw['status']
        self.status = ' **(VOADO)**' if self.flightFlown else '**(CANCELADO)**' if self.add_status[0] == '21' else ''

    def __str__(self):
        return f'{self.flight}: {self.departureAirport} - {self.arrivalAirport} {self.departureDate} {self.status}'


if __name__ == '__main__':
    url = 'https://myb.flytap.com/my-bookings/details/m2ynra/costaTeixeira'
    scrapper = TapScrapper()
    reservation = scrapper.get_reservation_details(url)
    assert len(reservation) == 1
    flight = reservation[0]
    assert isinstance(flight, Trip)
    print('tests passed')