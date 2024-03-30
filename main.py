import time

import multiprocessing
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
    # def __init__(self, url: str):
    #     self.url = url

    @staticmethod
    def settings():
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--ignore-certificate-errors")
        # options.add_argument("start-maximized")

        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # # Пробуем избежать вывода сообщений об уставершей версии в консоль
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_experimental_option('useAutomationExtension', False)
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
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "title"))
        )
        html = driver.page_source
        return html

    @staticmethod
    def update(block):
        link = 'https://www.avito.ru/' + block.a['href']
        name = block.a['title']
        cost = block.find('strong', {'class': 'styles-module-root-LIAav'}).get_text(strip=True)
        city = block.find('div', {'class': 'geo-root-zPwRk'}).get_text(strip=True)
        time_ = block.find('div', {'class': 'iva-item-dateInfoStep-_acjp'}).get_text(strip=True)
        return link, name, cost, city, time_

    def test(self, url_):
        time.sleep(3)
        driver = self.settings()
        driver.get(url=url_)
        try:
            while True:
                start_time = time.time()

                site_name = url_.replace('https://', '').split('/')[0]

                content = self.checker(driver)
                soup = BeautifulSoup(content, 'lxml')
                title = soup.find('title').get_text(strip=True)
                end_time = time.time()
                print(f"Время выполнения итерации для ресурса {site_name}...  {end_time - start_time} секунд,"
                      f"\n title - {title}")
                time.sleep(1)
        except Exception as e:
            print(e)
            driver.quit()

    def monitoring(self, url_):
        driver = self.settings()
        driver.get(url=url_)

        try:
            car_data = {}
            while True:
                start_time = time.time()
                content = self.checker(driver)
                soup = BeautifulSoup(content, 'lxml')
                blocks = soup.find_all('div', {'data-marker': 'item'})
                print(f'Блоков - {len(blocks)}')
                print(len(car_data))
                if car_data:
                    for block in blocks:
                        link, name, cost, city, time_ = self.update(block)
                        if link in car_data:
                            continue
                        else:
                            message(f'{name} {cost} {link}')
                            car_data[link] = f'{name}, цена: {cost}'
                else:
                    for block in blocks:
                        link, name, cost, city, time_ = self.update(block)
                        car_data[link] = f'{name}, цена: {cost}'
                        print(name)
                end_time = time.time()
                print(f"Время выполнения итерации {end_time - start_time} секунд")
                time.sleep(1)
        except Exception:
            driver.quit()


if __name__ == "__main__":
    url_1 = 'https://www.avito.ru/staryy_oskol/avtomobili?f=ASgCAgECAUXGmgwbeyJmcm9tIjo0MDAwMDAsInRvIjo4MDAwMDB9&localPriority=0&radius=200&searchRadius=200'
    url_2 = 'https://centerkrep.ru/krepezh/bolty-i-shpilki/bolty-mebelnye/bolt-mebelnyy-din-603-8kh90/'
    url_3 = 'https://habr.com/ru/articles/726218/'
    url_4 = 'https://firmax.info/?utm_source=yandex_Firmax&utm_medium=cpc&utm_campaign=Firmax_Poisk&utm_term=ST:search|S:none|AP:no|PT:other|P:4|DT:desktop|RI:10649|RN:%D0%A1%D1%82%D0%B0%D1%80%D1%8B%D0%B9%20%D0%9E%D1%81%D0%BA%D0%BE%D0%BB|CI:101322759|GI:5337581515|PI:48529703531|AI:15406878750|KW:%D0%BC%D0%B5%D0%B1%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%BB%D0%B5%D0%BA%D1%82%D1%83%D1%8E%D1%89%D0%B8%D0%B5&utm_content=15406878750&yclid=647627714219212799'
    url_5 = 'https://stroybat.ru/krepezh/bolty-din-603-mebelnye/bolt-mebel-nyj-din603-ocink-8h-90-s-gajkoj-2-sht/'
    url_list = [url_1, url_2, url_3, url_4, url_5]

    ap = AvitoParse()
    with multiprocessing.Pool(processes=5) as p:
        p.map(ap.test, url_list)

    # ap = AvitoParse()
    # ap.test(url_4)

