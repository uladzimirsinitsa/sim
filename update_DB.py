
import os
import sys
import time

from deta import Deta

from dotenv import load_dotenv

load_dotenv()

db = Deta(os.environ['KEY']).Base(os.environ['NAME_DB'])


def read_urls_from_file():
    with open('C:\data\data.csv', 'r') as f:
        yield from f.readlines()
    

def update_DB(url) -> None:
    updates = {
        'status_url':  'need_to_check',
    }
    db.update(updates, key=url)


def main():
    counter = 0
    urls = read_urls_from_file()
    try:
        while any(urls):
            url = next(urls).strip()
            update_DB(url)
            counter += 1
            print(counter)
            time.sleep(0.01)
    except:
        sys.exit()


if __name__ == '__main__':
    main()
    