#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Giannis Damilatis'
__version__ = '1.0.0'


from requests import Session
import sys


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


class classHomeworld(object):

    def __init__(self, session, url, params):
        self.session = session
        self.url = url
        self.homeworld = None
        self.params = params
        self.earth_orbital_period = 365.25
        self.earth_rotation_period = 24

    def connect(self):
        pass


class SearchCharacter(object):
    def __init__(self, session, url, params, worldFlag):
        self.session = session
        self.worldFlag = worldFlag
        self.url = url
        self.data = None
        self.character = {
            'name': None,
            'height': None,
            'mass': None,
            'birth_year': None,
            'world': None,
            'population': None,
            'correlation': None,
        }
        self.params = params

    def parseData(self, data, worldFlag):
        if (worldFlag):
            data = data.json().get('result')[0].get('properties')
            self.character['name'] = data.get('name')
            self.character['height'] = data.get('height')
            self.character['mass'] = data.get('mass')
            self.character['birth_year'] = data.get('birth_year')

    def connect(self):
        response = self.session.get(self.url, params=self.params)
        if response.status_code == 200 or response.status_code == 304:
            self.data = response.json().get('result')
            if not self.data:
                return True
            if self.data.len() > 0:
                self.data = self.parseData(self.data, self.worldFlag)
            # self.data = response.json().get('result')[0].get('properties')
            # self.character['name'] = self.data.get('name')
            # self.character['height'] = self.data.get('height')
            # self.character['mass'] = self.data.get('mass')
            # self.character['birth_year'] = self.data.get('birth_year')
            return True
        else:
            return False


class Character(object):

    def __init__(self, name, world):
        self.name = name
        self.world = world
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
        self.find_all_params = {
            'page': '1',
            'limit': '100',
        }

        self.params = {
            'name': self.name,
        }

        self.characters = None
        self.character = None

    def main(self):
        connector = Connector(self.session, self.base_url,
                              self.find_all_params)
        if not connector.connect():
            raise Exception('Cannot connect to the API')
        self.characters = getattr(connector, 'characters')
        if not self.characters:
            raise Exception('No characters found')
        # print(self.characters)

        connector = SearchCharacter(self.session, self.base_url,
                                    self.params, self.world)
        if not connector.connect():
            raise Exception('Cannot connect to the API')
        self.character = getattr(connector, 'character')
        self.character_data = getattr(connector, 'data')
        if not self.character_data:
            print('The force is not strong within you')
            sys.exit()
        if self.character_data:
            print("Name: ", self.character['name'])
            print("Height: ", self.character['height'])
            print("Mass: ", self.character['mass'])
            print("Birth Year: ", self.character['birth_year'])

# if __name__ == '__main__':
#     character = Character(self, name)
#     character.main()
