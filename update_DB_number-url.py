
import os
import sys
import time

import pymongo

from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()

SERVER = os.environ['SERVER']
PATH_FILES = os.environ['PATH_FILES']

client = pymongo.MongoClient(SERVER, serverSelectionTimeoutMS=5000)
db = client.records
numbers = db.numbers


def create_list_names() -> list:
    for _, _, names in os.walk(PATH_FILES):
        return names


def parse_url(names):
    count = 0
    for name in names:
        print(name)
        print(count)
        with open(f'{PATH_FILES}{name}') as file:
            text = file.read()
            soup = BeautifulSoup(text, 'lxml')
            url = soup.find('link', rel='canonical').get('href')
            numbers.insert_one({name: url})
            count += 1


def main():
    names = create_list_names()
    parse_url(names)


if __name__ == '__main__':
    main()
