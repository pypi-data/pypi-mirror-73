import re

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from unidecode import unidecode

import logging


class LoginPage(object):
    USERNAME_ELEM_ID = 'ctl00_ContentPlaceHolder1_txtLogin'
    PASSWORD_ELEM_ID = 'ctl00_ContentPlaceHolder1_txtSenha'
    SUBMIT_ELEM_ID = 'ctl00$ContentPlaceHolder1$btnLogar'
    LOGIN_URL = "https://cei.b3.com.br/CEI_Responsivo/"
    LOGGER = logging.getLogger("LoginPage")

    def __init__(self, driver, username, password, logger=None):
        self.driver = driver
        self.username = username
        self.password = password
        self.logger = logger

    def login(self):
        self.LOGGER.info('START')
        self.driver.find_element_by_id(self.USERNAME_ELEM_ID).send_keys(self.username)
        self.driver.find_element_by_id(self.PASSWORD_ELEM_ID).send_keys(self.password)
        self.driver.find_element_by_name(self.SUBMIT_ELEM_ID).click()
        self._insecure_bypass()

        self.LOGGER.info('END')
        return HomePage(self.driver)

    def _insecure_bypass(self):
        try:
            self.driver.find_element_by_id("exceptionDialogButton").click()
        except:
            pass


class HomePage(object):
    ASSETS_EXTRACT_PATH = 'negociacao-de-ativos.aspx'
    LOGGER = logging.getLogger("HomePage")

    def __init__(self, driver):
        self.driver = driver

    def go_to_extract_page(self):
        self.LOGGER.info('START')
        self.driver.execute_script("window.location.href = '" + self.ASSETS_EXTRACT_PATH + "'")
        self.LOGGER.info('END')
        return ExtractPage(self.driver)


class ExtractPage(object):
    LOGGER = logging.getLogger("ExtractPage")
    BROKERS_SELECTION_ID = 'ctl00_ContentPlaceHolder1_ddlAgentes'
    INQUIRY_BUTTON_ID = 'ctl00_ContentPlaceHolder1_btnConsultar'

    def __init__(self, driver):
        self.driver = driver

    def get_all_brokers_extract(self):
        self.LOGGER.info('START')

        broker_selection_options = Select(
            self.driver.find_element_by_id(self.BROKERS_SELECTION_ID)).options

        all_extracts = []
        for index, elem in enumerate(broker_selection_options[1:], 1):
            stock_brokers_selection = Select(self.driver.find_element_by_id(self.BROKERS_SELECTION_ID))
            broker_name = stock_brokers_selection.options[index].text
            self.LOGGER.info(f'Selecting {broker_name} broker')
            stock_brokers_selection.select_by_index(index)
            WebDriverWait(self.driver, 10).until(
                expected_conditions.element_to_be_selected(
                    stock_brokers_selection.options[index]
                ))
            inquire_button = self.driver.find_element_by_id(self.INQUIRY_BUTTON_ID)
            inquire_button.click()

            all_extracts = all_extracts + self._parse_broker_extract(broker_name)
            self.driver.refresh()
        self.LOGGER.info('END')
        return all_extracts

    def _parse_broker_extract(self, broker_name):
        tables = self.driver.find_elements_by_xpath("//table")
        if len(tables) != 2:
            return []

        extract_table = tables[0]
        rows = extract_table.find_elements_by_tag_name('tr')

        if len(rows) <= 1:
            return []

        headers = [cell.text for cell in rows[0].find_elements_by_xpath('./*')]
        rows = [[cell.text for cell in row.find_elements_by_xpath('./*')] for row in rows[1:]]

        result = []
        for row in rows:
            row_dict = {}
            for index, elem in enumerate(row):
                key = self._pythonfy_text(headers[index])
                row_dict[key] = unidecode(elem).replace(',', '.')
            row_dict['corretora'] = broker_name
            result.append(row_dict)

        return result

    @staticmethod
    def _pythonfy_text(text):
        new_text = text.replace('(R$)', '').strip()
        return re.sub(r'[ /]', "_", unidecode(new_text).lower())
