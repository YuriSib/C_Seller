import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class AvitoParse:
    def __init__(self, url: str):
        self.url = url

    @staticmethod
    def settings():
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
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

    def monitoring(self):
        driver = self.settings()
        driver.get(url=self.url)

        try:
            while True:
                content = self.checker(driver)
                time.sleep(5)
        except Exception:
            driver.quit()


url_ = 'https://www.avito.ru/staryy_oskol/avtomobili?radius=200&searchRadius=200'
ap = AvitoParse(url_)
ap.monitoring()