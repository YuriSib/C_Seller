import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tg_master import message


class AvitoParse:
    def __init__(self, url: str):
        self.url = url

    @staticmethod
    def settings():
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        # options.binary_location = '/usr/bin/google-chrome'
        # options.add_argument("--headless")
        options.headless = True
        options.add_argument("start-maximized")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # Пробуем избежать вывода сообщений об уставершей версии в консоль
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        return driver

    @staticmethod
    def checker(driver):
        driver.refresh()
        html = driver.page_source
        return html

    @staticmethod
    def update(block):
        link = 'https://www.avito.ru/' + block.a['href']
        name = block.a['title']
        cost = block.find('strong', {'class': 'styles-module-root-LIAav'}).get_text(strip=True)
        city = block.find_all('div', {'class': 'geo-root-zPwRk'}).get_text(strip=True)
        time_ = block.find_all('div', {'class': 'iva-item-dateInfoStep-_acjp'}).get_text(strip=True)
        return link, name, cost, city

    def monitoring(self):
        driver = self.settings()
        driver.get(url=self.url)

        try:
            car_data = {}
            while True:
                content = self.checker(driver)
                soup = BeautifulSoup(content)
                blocks = soup.find_all('div', {'data-marker': 'item'})
                print(len(car_data))

                if car_data:
                    for block in blocks:
                        link, name, cost, city = self.update(block)

                        if link in car_data:
                            continue
                        else:
                            message(f'{name} {cost} {link}')
                            car_data[link] = f'{name}, цена: {cost}'
                else:
                    for block in blocks:
                        link, name, cost, city = self.update(block)
                        car_data[link] = f'{name}, цена: {cost}'

                time.sleep(1)
        except Exception:
            driver.quit()


url_ = 'https://www.avito.ru/staryy_oskol/avtomobili?f=ASgCAgECAUXGmgwbeyJmcm9tIjo0MDAwMDAsInRvIjo4MDAwMDB9&localPriority=0&radius=200&searchRadius=200'
ap = AvitoParse(url_)
ap.monitoring()