from selenium import webdriver


class TapScrapper:

    def __init__(self, max_wait=10):
        self._driver = webdriver.Chrome()
        self._max_wait = max_wait
        self.components = []

    def get_reservation_details(self, url):
        self._driver.get(url)
        self._get_reservation_components()
        return [FlightInfo(text) for text in self.components_text]

    def _get_reservation_components(self):
        for i in range(1, self._max_wait + 1):
            self._driver.implicitly_wait(1)
            self.components = self._driver.find_elements_by_tag_name('app-extras-flight')
            self.components_text = [component.text for component in self.components]
            if len(self.components_text) > 0 and len(self.components_text[0]) > 7:
                break
            if i >= self._max_wait:
                raise Exception('waited for to long')


class FlightInfo:
    def __init__(self, component_text):
        self.raw = component_text
        info = component_text.replace('Cancelado\n', '').replace('Voado\n', '').split('\n')
        from_to = info[0]
        split = from_to.find('para')
        self.status = self._get_status()
        self.flight_number = info[7]
        self.from_location = info[3] + ' - ' + from_to[:split - 1]
        self.to_location = info[5] + ' - ' + from_to[split + 5:]
        self.date = info[1][:17] + ' at ' + info[2]
        self.arrival_time = info[4]
        self.trip_length = info[6]

    def _get_status(self):
        status = 'Cancelado' if self.raw.find('cancelado') > 0 else 'Ativo'
        if self.raw.find('Voado') > 0:
            status = 'Voado'
        return status

    def comment(self):
        comment = ''
        comment += f'##Flight Number: {self.flight_number}\n'
        comment += f'###Status: {self.status}\n'
        comment += f'From: {self.from_location}\n'
        comment += f'To: {self.to_location}\n'
        comment += f'Date: {self.date}\n'
        comment += f'Arrival Time: {self.arrival_time}\n'
        comment += f'Trip Length: {self.trip_length}\n'
        return comment
