from selenium import webdriver


url = 'https://www.cyberforum.ru/'

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)
driver.get(url=url)
driver.quit()