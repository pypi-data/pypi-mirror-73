import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from cei_crawler.pages import LoginPage

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s.%(funcName)s %(levelname)-s: %(message)s')


class CEICrawler(object):
    CEI_URL = "https://cei.b3.com.br/CEI_Responsivo/"
    IMPLICITLY_WAIT_SECONDS = 10
    LOGGER = logging.getLogger("CEICrawler")

    def __init__(self, username, password):
        self.username = username
        self.password = password

        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.driver.get(self.CEI_URL)

    def get_assets_negotiation_extract(self):
        login_page = LoginPage(self.driver, self.username, self.password)
        home_page = login_page.login()
        extract_page = home_page.go_to_extract_page()
        return extract_page.get_all_brokers_extract()

    def __del__(self):
        self.driver.close()
