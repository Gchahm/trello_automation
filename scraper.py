from selenium import webdriver
import util


def get_flight_details(url, max_wait=10):
    driver = webdriver.Chrome()
    driver.get(url)
    components = get_flight_component(driver, 0, max_wait)
    result = get_components_info(components)
    driver.close()
    return result


def get_flight_component(driver, tries, max_wait):
    driver.implicitly_wait(tries)
    try:
        driver.find_element_by_tag_name('app-extras-flight')
        elements = driver.find_elements_by_tag_name('app-extras-flight')
        return elements
    except:
        if tries > max_wait:
            raise Exception('waited for to long')
        return get_flight_component(driver, tries + 1, max_wait)


def get_components_info(components):
    result = []
    for component in components:
        result.append(get_flight_info(component))
    return result


def get_flight_info(component):
    status = 'Cancelado' if component.text.find('cancelado') > 0 else 'Ativo'
    info = component.text.replace('Cancelado\n', '').split('\n')
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


if __name__ == '__main__':
    URL = 'https://myb.flytap.com/my-bookings/details/mr8dyf/BorgesdoNascimento'
    util.save_json_to_file(get_flight_details(URL), 'output.json')
