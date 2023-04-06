#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Giannis Damilatis'
__version__ = '1.0.0'


from requests import Session


class Connector(object):

    def __init__(self, session, url, params):
        self.session = session
        self.url = url
        self.characters = None
        self.params = params

    def connect(self):
        response = self.session.get(self.url, params=self.params)
        if response.status_code == 200 or response.status_code == 304:
            self.characters = response.json().get('results')
            return True
        else:
            return False


class Character(object):

    def __init__(self, name):
        self.name = name
        self.session = Session()
        self.base_url = 'https://www.swapi.tech/api/people'
        self.session.headers = {
            'authority': 'www.swapi.tech',
            'accept': 'text/html,application/xhtml+xml,\
            application/json,application/xml;q=0.9,\
            image/avif,image/webp,image/apng,*/*;q=0.8,\
            application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,el;q=0.8',
            'dnt': '1',
            'if-none-match': 'W/"38d-63EggyxMQsb/kvArRBntX5GVCzY"',
            'referer': 'https://www.swapi.tech/api',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8",\
            "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64;\
            x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0\
            .0.0 Safari/537.36',
        }
        self.params = {
            'page': '1',
            'limit': '100',
        }

        self.characters = None

    def main(self):
        connector = Connector(self.session, self.base_url, self.params)
        if not connector.connect():
            raise Exception('Cannot connect to the API')
        self.characters = getattr(connector, 'characters')
        if not self.characters:
            raise Exception('No characters found')
        print(self.characters)

# if __name__ == '__main__':
#     character = Character(self, name)
#     character.main()
