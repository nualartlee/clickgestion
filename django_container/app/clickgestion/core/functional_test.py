from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# Connect to a docker container running selenium on this network
selenium_url = 'http://selenium:4444/wd/hub'
capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
browser = webdriver.Remote(selenium_url, capabilities)
print('Browser ready')

# Set a wait object with timeout
wait = WebDriverWait(browser, 5)

# Request the site from the nginx container
url = 'http://nginx/'
browser.get(url)


assert 'ClickGestion' in browser.title
elem = browser.find_element_by_id('id_username')
elem.send_keys('dani')
elem = browser.find_element_by_id('id_password')
elem.send_keys('dani')
elem.send_keys(Keys.RETURN)
elem = browser.find_element_by_id('submit-id-submit')
elem.click()

print(browser.page_source)
import pdb;pdb.set_trace()

#try:
#    page_loaded = wait.until(lambda browser: 'login' in browser.current_url)
#except TimeoutException:
#   print("Loading timeout expired")
