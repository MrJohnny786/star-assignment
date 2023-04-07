#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Giannis Damilatis'
__version__ = '1.0.0'


from requests import Session
import sys
import json
from datetime import datetime
import os
import matplotlib.pyplot as plt


class Virtualise(object):
    def __init__(self):
        self.file_path = 'cache/advancedData.json'

    def main(self):
        if not os.path.isfile(self.file_path):
            return False
        with open(self.file_path, 'r') as f:
            data = json.load(f)

        x = []
        y = []
        z = []
        for _data in data['requests']:
            x.append(_data['search'])
            y.append(_data['time'])

            z.append(_data['result'])

        colors = ['red' if i == 'Unsuccessful' else 'green' for i in z]
        plt.scatter(x, y, c=colors)

        plt.title("Star wars search names/time graph")
        plt.ylabel('Time-Axis')

        plt.xlabel('Search name-Axis')

        plt.show()

        return True


class CacheHandler(object):

    def __init__(self):
        self.file_path = 'cache/advancedData.json'
        self.data = []
        self.request = {
            'requests': [],
            'total_data': {
                'total_requests': 0,
                'total_succesful': 0,
                'total_unsuccesful': 0,
            }
        }

    def initialize_cache_data(self):
        if os.path.isfile(self.file_path):
            return
        with open(self.file_path, 'w') as f:
            json.dump(self.request, f)
            return

    def update_json(self, data):
        if os.path.isfile(self.file_path):
            with open(self.file_path, 'r') as f:
                cached_data = json.load(f)
            cached_data['requests'].append(data)
            cached_data['total_data']['total_requests'] += 1
            if data['result'] == 'Successful':
                cached_data['total_data']['total_succesful'] += 1
            else:
                cached_data['total_data']['total_unsuccesful'] += 1
            with open(self.file_path, 'w') as f:
                json.dump(cached_data, f)


class Connector(object):

    def __init__(self, session, url, params):
        self.session = session
        self.url = url
        self.characters = {
            'data': None,
            'cached': None,
        }
        self.params = params

    def fetch_data(self, json_cache: str):
        try:
            with open('cache/'+json_cache, 'r') as f:
                self.characters = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return

    def connect(self):
        self.fetch_data('characters.json')
        if self.characters['data']:
            return True
        response = self.session.get(self.url, params=self.params)
        if response.status_code == 200 or response.status_code == 304:
            self.characters['data'] = response.json().get('results')
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.characters['cached'] = current_time
            with open('cache/characters.json', 'w') as f:
                json.dump(self.characters, f)
            return True
        else:
            return False


class classHomeworld(object):

    def __init__(self, session, url):
        self.session = session
        self.url = url
        self.homeworld = None
        self.earth_orbital_period = 365.25
        self.earth_rotation_period = 24
        self.world = {
            'name': None,
            'population': None,
            'orbital_period': None,
            'rotation_period': None,
            'correlation_day': None,
            'correlation_year': None,
        }

    def worlds_correlation(self, day, year):
        if day == 'unknown' or year == 'unknown':
            self.world['correlation_day'] = 'unknown'
            self.world['correlation_year'] = 'unknown'
            return
        self.world['correlation_day'] = round(
            int(day) / self.earth_rotation_period, 2)
        self.world['correlation_year'] = round(
            int(year) / self.earth_orbital_period, 2)
        return

    def connect(self):
        response = self.session.get(self.url)
        if response.status_code == 200 or response.status_code == 304:
            self.homeworld_data = response.json().get('result').get('properties')
            if not self.homeworld_data:
                return True
            self.world['name'] = self.homeworld_data.get('name')
            self.world['population'] = self.homeworld_data.get('population')
            self.world['orbital_period'] = self.homeworld_data.get(
                'orbital_period')
            self.world['rotation_period'] = self.homeworld_data.get(
                'rotation_period')

            self.worlds_correlation(
                self.world['rotation_period'], self.world['orbital_period'])
            return True
        else:
            return False


class SearchCharacter(object):
    def __init__(self, session, url, params, worldFlag):
        self.session = session
        self.worldFlag = worldFlag
        self.url = url
        self.world_data = None
        self.character = {
            'name': None,
            'height': None,
            'mass': None,
            'birth_year': None,
            'world_url': None,
            'world': None,
            'population': None,
            'correlation': {
                'day': None,
                'year': None,
            },
            'world_flag': worldFlag,
            'cached': None
        }
        self.params = params
        self.cache_values = {
            'search': None,
            'result': None,
            'time': None,
        }

    def fetch_data(self, json_cache: str):
        try:
            with open('cache/'+json_cache, 'r') as f:
                self.character = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return
            # print('no local cache found', e)

    def parseData(self, data, worldFlag):
        data = data[0].get('properties')
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.character['cached'] = current_time
        if (worldFlag):
            self.character['name'] = data.get('name')
            self.character['height'] = data.get('height')
            self.character['mass'] = data.get('mass')
            self.character['birth_year'] = data.get('birth_year')
            self.character['world_url'] = data.get('homeworld')

            connector = classHomeworld(
                self.session, self.character['world_url'])
            if not connector.connect():
                raise Exception('Cannot connect to the API for the worlds')

            self.world_data = getattr(connector, 'world')
            self.character['world'] = self.world_data.get('name')
            self.character['population'] = self.world_data.get('population')
            self.character['correlation']['day'] = self.world_data.get(
                'correlation_day')
            self.character['correlation']['year'] = self.world_data.get(
                'correlation_year')
            return self.character
        else:
            self.character['name'] = data.get('name')
            self.character['height'] = data.get('height')
            self.character['mass'] = data.get('mass')
            self.character['birth_year'] = data.get('birth_year')
            return self.character

    def connect(self):
        self.fetch_data(self.params['name']+'.json')
        if self.character['cached']:
            self.data = self.character
            return True
        cacheHandler = CacheHandler()

        response = self.session.get(self.url, params=self.params)
        if response.status_code == 200 or response.status_code == 304:
            self.data = response.json().get('result')
            if not self.data:
                self.cache_values['search'] = self.params['name']
                self.cache_values['result'] = 'Unsuccessful'
                self.cache_values['time'] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S")
                cacheHandler.update_json(self.cache_values)
                return True
            if len(self.data) > 0:
                self.data = self.parseData(self.data, self.worldFlag)
                self.cache_values['search'] = self.params['name']
                self.cache_values['result'] = 'Successful'
                self.cache_values['time'] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S")
                cacheHandler.update_json(self.cache_values)
                filename = 'cache/'+self.params['name']+'.json'
                with open(filename, 'w') as f:
                    json.dump(self.character, f)
            return True
        else:
            return False


class Character(object):

    def __init__(self, name=None, world=False, cache=False, virtualize=False):
        self.name = name
        self.world = world
        self.cache = cache
        self.virtualize = virtualize
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

    def remove_cache(self):
        folder_path = "cache"
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
                exit()

    def main(self):
        if self.virtualize:
            virtual = Virtualise()
            if not virtual.main():
                print('No data exist to virtualize')
                exit()
            exit()
        if self.cache:
            self.remove_cache()
            print('Removed cache')
            exit()
        cacheHandler = CacheHandler()
        cacheHandler.initialize_cache_data()
        connector = Connector(self.session, self.base_url,
                              self.find_all_params)
        if not connector.connect():
            raise Exception('Cannot connect to the API')
        self.characters = getattr(connector, 'characters')
        if not self.characters['data']:
            raise Exception('No characters found')

        connector = SearchCharacter(self.session, self.base_url,
                                    self.params, self.world)
        if not connector.connect():
            raise Exception('Cannot connect to the API')
        self.character = getattr(connector, 'character')
        self.character_data = getattr(connector, 'data')
        if not self.character_data:
            print('The force is not strong within you')
            sys.exit()
        if self.character_data and self.character_data.get('world_flag'):
            print("Name: ", self.character.get('name'))
            print("Height: ", self.character.get('height'))
            print("Mass: ", self.character.get('mass'))
            print("Birth Year: ", self.character.get('birth_year'))
            print('                                  ')
            print("Homeworld")
            print("----------------------------------")
            print("Name: ", self.character.get('world'))
            print("Population: ", self.character['population'])
            print('                                  ')
            print('On', self.character['world'], '1 year on earth is', self.character.get('correlation')
                  .get('year'), 'years and 1 day', self.character.get('correlation').get('day'), 'days')
            print('                                  ')
            if self.character.get('cached'):
                print('cached: ', self.character['cached'])
        else:
            print("Name: ", self.character.get('name'))
            print("Height: ", self.character.get('height'))
            print("Mass: ", self.character.get('mass'))
            print("Birth Year: ", self.character.get('birth_year'))
            print('                                  ')
            if self.character.get('cached'):
                print('cached: ', self.character['cached'])
