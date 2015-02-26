#!/usr/bin/env python
import time

import requests

from lxml.html import fromstring
from pync import Notifier

ENDPOINT = 'http://macroom.com.ua/products/apple-macbook-pro-15-with-retina-display-2014-mgxa2'
TIMEOUT = 60
XPATH = '/html/body/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[5]'
TITLE = 'MGXA2 price '


def main():
    last_currency = None

    while True:
        try:
            html = requests.get(ENDPOINT).text
            tree = fromstring(html)
            el = tree.get_element_by_id('price-val')
            value = float(el.text.replace(',', '.'))
        except Exception:
            time.sleep(TIMEOUT)
            continue

        if last_currency != value:
            last_currency = value

            try:
                Notifier.notify(
                    str(value),
                    open=ENDPOINT,
                    title=TITLE
                )
            except Exception:
                pass

        time.sleep(TIMEOUT)


if __name__ == '__main__':
    main()
