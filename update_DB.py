
import os
import sys
import time
from typing import Generator
from deta import Deta


db = Deta(os.environ['KEY']).Base(os.environ['NAME_DB'])


def read_urls_from_file() -> Generator[str]:
    with open('C:\processed_urls', 'r') as f:
        yield from f.readlines()
    

def update_DB(url) -> None:
    updates = {
        'status_url':  'processed',
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
            time.sleep(3)
    except:
        sys.exit()


if __name__ == '__main__':
    main()
    