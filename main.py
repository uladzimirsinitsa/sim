
import os
import sys
import time
import pickle
from typing import Generator

from deta import Deta
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from dotenv import load_dotenv


load_dotenv()


db = Deta(os.environ['KEY']).Base(os.environ['NAME_DB'])


def get_url() -> Generator:
    urls = db.fetch([{'status_url': 'need_to_check'}], limit=10).items
    # urls = db.fetch([{'status_url': 'need_to_check'}, {'number_CPU': 2}], limit=10).items

    yield from urls


def update_DB(url) -> None:
    updates = {
        'status_url':  'processed',
    }
    db.update(updates, key=url)


service = Service(os.environ['PATH_DRIVER'])
driver = webdriver.Firefox(service=service)
driver.get(os.environ['URL'])
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)


def parsing_data_for_file_naming() -> str:
    name = driver.find_element(
                By.XPATH,
                '//*[@id="pageOuter"]/div/div[3]/div[2]/table/tbody/tr[1]/td[2]/h1'
                ).text
    id = driver.find_element(By.TAG_NAME, 'h2').text
    data = (name, id)
    return '_'.join(data)


def safe_file(name_file, html_data) -> None:
    with open(f'C:\data\{name_file}', 'w', encoding="utf-8") as f:
            f.write(html_data)
    

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
            update_DB(url)
            try:
                name_file = parsing_data_for_file_naming()
            except:
                continue
            html_data = driver.page_source
            safe_file(name_file, html_data)
            time.sleep(4)
    except:
        driver.quit()
        sys.exit()


if __name__ == '__main__':
    main()
    