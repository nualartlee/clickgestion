from selenium import webdriver

# Connect to a docker container running selenium on this network
url = 'http://selenium:4444/wd/hub'
capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
browser = webdriver.Remote(url, capabilities)
print('Browser ready')

# Request the site from the nginx container
browser.get('http://clickgestion_nginx_1')

assert 'ClickGestion' in browser.title