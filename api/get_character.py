#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Giannis Damilatis'
__version__ = '1.1.0'

from requests import Session
import json
import os
import time
import datetime

class Character(object):

    def __init__(self, name):
        self.name = name
        self.session = Session()
        self.base_url = 'https://www.swapi.tech/api'
        self.headers = {
            'authority': 'www.swapi.tech',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,el;q=0.8',
            'dnt': '1',
            'if-none-match': 'W/"38d-63EggyxMQsb/kvArRBntX5GVCzY"',
            'referer': 'https://www.swapi.tech/api',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
        self.data = None

    def main(self):
         response = self.session.get(self.url, headers=self.headers)

         if not response.ok:
             raise Exception('Cannot connect to the star wars api')

if __name__ == '__main__':
    import sys
    sys.path.append('..')