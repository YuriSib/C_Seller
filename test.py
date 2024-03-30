# from selenium import webdriver

# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('--no-sandbox')
# driver = webdriver.Chrome(options=options)
#
# driver.get('https://www.cyberforum.ru/')
#
# html = driver.page_source
# print(html)
# driver.quit()

import ssl
import requests
from requests_html import HTMLSession


url = 'https://www.avito.ru/staryy_oskol/avtomobili?f=ASgCAgECAUXGmgwbeyJmcm9tIjo0MDAwMDAsInRvIjo4MDAwMDB9&p=1&radius=200&searchRadius=200'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

session = HTMLSession()
response = session.get()
response.html.render()
print(response)