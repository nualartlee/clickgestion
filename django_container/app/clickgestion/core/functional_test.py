from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from django.test import TestCase


class FunctionalTestCase(TestCase):

    site_url = 'http://nginx/'
    selenium_url = 'http://selenium:4444/wd/hub'
    _browser = None

    def setUp(self):
        test_name = self._testMethodName
        print('\n\n      ---- %s ----\n' % test_name)

    @classmethod
    def setUpTestData(cls):
        print("\n\n============ %s ===============\n\n" % cls.__name__)

    def open_selenium_firefox_browser(self):
        """
        Connects to a selenium docker container and opens a firefox browser.

        :return: A selenium browser object
        """
        capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
        self._browser = webdriver.Remote(self.selenium_url, capabilities)
        print('Browser ready')
        return self._browser

    @property
    def browser(self):
        """
        Get the browser in use for this test case.

        :return: A selenium browser object (firefox by default)
        """
        if not self._browser:
            return self.open_selenium_firefox_browser()
        return self._browser

    def login(self, username, password):
        """
        Login with the given username and password.

        :param username:
        :param password:
        :return:
        """
        # Navigate to login
        self.browser.get(self.site_url + 'login')
        elem = self.browser.find_element_by_id('id_username')
        elem.send_keys('dani')
        elem = self.browser.find_element_by_id('id_password')
        elem.send_keys('dani')
        elem.send_keys(Keys.RETURN)
        elem = self.browser.find_element_by_id('submit-id-submit')
        elem.click()
        print(self.browser.page_source)
        import pdb;pdb.set_trace()


if __name__ == "__main__":
    test_case = FunctionalTestCase()
    test_case.login('dani', 'dani')

