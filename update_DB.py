
import os
import sys
import time

import pymongo

from dotenv import load_dotenv

load_dotenv()


SERVER = os.environ['SERVER']

client = pymongo.MongoClient(SERVER, serverSelectionTimeoutMS=5000)
db = client.records_DB
urls = db.urls


def update_DB(list_2: list):
    urls.insert_one({'url': list_2})


def read_urls_from_file():
    with open('C:\data\data.csv', 'r') as f:
        return f.readlines()


def main():
    list_1 = read_urls_from_file()
    list_2 = [url.strip('\n') for url in list_1]
    update_DB(list_2)
    print('finish')
    sys.exit()


if __name__ == '__main__':
    main()
