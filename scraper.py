from selenium import webdriver
import logging


class TapScrapper:

    def __init__(self, max_wait=10):
        self._driver = webdriver.Chrome()
        self._max_wait = max_wait
        self.components = []

    def get_reservation_details(self, url):
        self._driver.get(url)
        self._get_reservation_components()
        return [parse_flight_info(text) for text in self.components_text]

    def _get_reservation_components(self):
        for i in range(1, self._max_wait + 1):
            self._driver.implicitly_wait(1)
            self.components = self._driver.find_elements_by_tag_name('app-extras-flight')
            self.components_text = [component.text for component in self.components]
            if len(self.components_text) > 0 and len(self.components_text[0]) > 7:
                break
            if i >= self._max_wait:
                raise Exception('waited for to long')


def parse_flight_info(component_text):
    logging.debug('Component Text: ' + '|'.join(component_text.split('\n')))
    status = 'Cancelado' if component_text.find('cancelado') > 0 else 'Ativo'
    if component_text.text.find('Voado') > 0:
        status = 'Voado'
    info = component_text.replace('Cancelado\n', '').replace('Voado\n', '').split('\n')
    from_to = info[0]
    split = from_to.find('para')
    return {
        'flight_number': info[7],
        'status': status,
        'from': info[3] + ' - ' + from_to[:split - 1],
        'to:': info[5] + ' - ' + from_to[split + 5:],
        'date': info[1][:17] + ' at ' + info[2],
        'arrival_time': info[4],
        'trip_length': info[6],
    }
