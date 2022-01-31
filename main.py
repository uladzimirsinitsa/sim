
import os
import sys
import time
import pickle

import pymongo

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from bs4 import BeautifulSoup


load_dotenv()

SERVER = os.environ['SERVER']
PATH_DRIVER = os.environ['PATH_DRIVER']
URL = os.environ['URL']
DOMAIN = os.environ['DOMAIN']

client = pymongo.MongoClient(SERVER, serverSelectionTimeoutMS=5000)
db = client.records_DB

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
    with open(f'C:\data\data\{name}', 'w', encoding="utf-8") as file:
        file.write(text)


def main() -> None:
    urls = db.urls.find_one()['url']
    for url in urls:
        driver.get(url)
        try:
            text, name = parsing_data_for_file_naming()
            print('\a')
            time.sleep(60)
        except AttributeError:
            continue
        safe_file(name[len(DOMAIN):], text)
        time.sleep(7)
    driver.quit()
    sys.exit()


if __name__ == '__main__':
    main()
