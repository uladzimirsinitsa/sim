
import os
import sys
import time
import pickle

from deta import Deta
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from bs4 import BeautifulSoup


load_dotenv()
db = Deta(os.environ['KEY']).Base(os.environ['NAME_DB'])


PATH_DRIVER = os.environ['PATH_DRIVER']
URL = os.environ['URL']
DOMAIN = os.environ['DOMAIN']


def get_url():
    urls = db.fetch([{'status_url': 'need_to_check'}], limit=10).items
    yield from urls


def update_DB(url) -> None:
    updates = {
        'status_url':  'processed',
    }
    db.update(updates, key=url)


service = Service(PATH_DRIVER)
driver = webdriver.Firefox(service=service)
driver.get(URL)
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)


def parsing_data_for_file_naming() -> tuple:
    text = driver.page_source
    soup = BeautifulSoup(text, 'lxml')
    name = soup.find('link', rel='canonical').get('href')
    return text, name


def safe_file(name, text) -> None:
    with open(f'C:\\Users\\God\\Desktop\\Drive\\data\\{name}', 'w', encoding="utf-8") as file:
        file.write(text)


def main():
    try:
        urls = get_url()
        while True:
            try:
                url = next(urls)['url']
            except StopIteration:
                time.sleep(1)
                main()
            driver.get(url)
            text, name = parsing_data_for_file_naming()
            safe_file(str(name[len(DOMAIN):]), text)
            update_DB(url)
            time.sleep(4)
    except:
        driver.quit()
        sys.exit()


if __name__ == '__main__':
    main()
