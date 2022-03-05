from alive_progress import alive_bar
from json import JSONDecodeError
from fake_useragent import UserAgent
from datetime import datetime
from functools import reduce
from random import randint
from random import seed
import requests
import pandas as pd
import random
import timeit
import time

import numpy as np
import pickle
import urllib

import pickle
import json
import os
import math
import asyncio
from urllib.error import HTTPError
import aiohttp
import platform
from datetime import datetime
import requests
import statistics
from aiohttp import ClientSession
import matplotlib.pyplot as plt

# TODO
# Add semaphores
# Change request headers
# Include more filtering possibly 
# Use progressbars (tqdm)
class PegaxyExtractor:

    def __init__(self):
        self.data = []
        self.filename = 'all_pegas {}.pkl'.format(datetime.now().strftime("%Y%m%d"))

        self.url1 = "https://api-apollo.pegaxy.io/v1/game-api/market/pegasListing/{id}?gender=Male&sortType=ASC&sortBy=price&currency=0xc2132D05D31c914a87C6611C10748AEb04B58e8F&isAuction=false&breedTime[0]=0"
        self.url2 = "https://api-apollo.pegaxy.io/v1/game-api/market/pegasListing/{id}?&marketType=FixedPrice&currency=0xc2132D05D31c914a87C6611C10748AEb04B58e8F&breedFrom=0&breedTo=7"
        self.url3 = "https://api-apollo.pegaxy.io/v1/game-api/market/listing/{id}"
        self.url_race_history = "https://api-apollo.pegaxy.io/v1/game-api/race/history/pega/{id}"
        
        # ua = UserAgent()
        # header = {'User-Agent':str(ua.firefox)}
        # ua.random

        user_agent_list = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            # ua.chrome,
            # ua.firefox
        ]

    def get_count(self):

        # url = f"https://api-apollo.pegaxy.io/v1/game-api/market/pegasListing/{id}?gender=Male&sortType=ASC&sortBy=price&currency=0xc2132D05D31c914a87C6611C10748AEb04B58e8F&isAuction=false&breedTime[0]=0"
        url = "https://api-apollo.pegaxy.io/v1/game-api/market/pegasListing/marketType=FixedPrice&currency=0xc2132D05D31c914a87C6611C10748AEb04B58e8F&breedFrom=0&breedTo=7"
        r = requests.get(url)

        # r = requests.get(self.url1)

        print("Getting {} Pegas, {} pages".format(r.json()['total'], math.ceil(r.json()['total'] / 12)))
        return math.ceil(r.json()['total'] / 12)


    def get_rent_history(self, id=173682):
        r = requests.get(self.url_race_history.format(id))

        data = r.json()
        totals = { 'wins': 0, 'total_races': 0, 'total_reward': 0}
        for idx, race in enumerate(data['data']):
            print("Race {}: {}".format(idx+1, datetime.fromtimestamp(race['race']['end'])))

            if race['position'] >= 4:
                totals['total_races'] += 1
            else:
                totals['wins'] += 1
                totals['total_reward'] += race['reward']

        print("Win rate: {}, Total reward: {}".format(totals['wins']/ totals['total_races'], totals['total_reward']))
        print(totals)

    def transform(self, data):
        pega_details = []

        for idx, iteration in enumerate(data):
            try:
                for pega in iteration:
                    pega_details.append(pega)
            except Exception as e:
                print("Error in idx {}: {}".format(idx, e))

            
                
        self.save(pega_details)

    def save(self, data, filename=None):
        if filename is None:
            filename = self.filename

        file = open(filename, 'wb')
        pickle.dump(data, file)
    def load(self, filename=None):
        if filename is None:
            filename = self.filename
        with open(filename, 'rb') as f:
            pega_details = pickle.load(f) 
        return pega_details

    async def get_pega(
        self,
        session: aiohttp.ClientSession,
        id: int,
        **kwargs
    ) -> dict:        
        url = f"https://api-apollo.pegaxy.io/v1/game-api/market/listing/{id}"
        # url = f"https://api-apollo.pegaxy.io/v1/game-api/pega/{id}"
        response = await session.request('GET', url=url, **kwargs)
        details = await response.json()
        return details
    async def get_market_pegas(
        self,
        session: aiohttp.ClientSession,
        id: int,
        **kwargs
    ) -> dict:

        url = f"https://api-apollo.pegaxy.io/v1/game-api/market/pegasListing/{id}?&marketType=FixedPrice&currency=0xc2132D05D31c914a87C6611C10748AEb04B58e8F&breedFrom=0&breedTo=7"
        # url = f"https://api-apollo.pegaxy.io/v1/game-api/market/pegasListing/{id}?gender=Male&sortType=ASC&sortBy=price&currency=0xc2132D05D31c914a87C6611C10748AEb04B58e8F&isAuction=false&breedTime[0]=0"


        response = await session.request('GET', url=url, **kwargs)
        # Note that this may raise an exception for non-2xx responses
        # You can either handle that here, or pass the exception through
        data = await response.json()

        return data['market']        

    

    async def start(self, pages):
        async with ClientSession() as session:
            tasks = [] 

            for i in range(pages):
                tasks.append(self.get_market_pegas(session=session, id=i))

            data = await asyncio.gather(*tasks, return_exceptions=True)
            self.transform(data)
    async def get_deets(self):
        async with ClientSession() as session:
            tasks = [] 

            pegas = self.load()

            for pega in pegas:
                tasks.append(self.get_pega(session=session, id=pega['id']))

            data = await asyncio.gather(*tasks, return_exceptions=True)
            self.save(data)

    

if __name__ == '__main__':
    ext = PegaxyExtractor()

    ext.get_rent_history()
# Start Extraction
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(ext.start(ext.get_count()))
    # asyncio.run(ext.get_deets())
    
    
# Start Transformation
    ## pegas = [pega['nft']['win_rate'] = "{:.4f}".format(win_rate * 100) for pega in pegas if 'nft' in pega]
    
    # pegas = ext.load('all_pegas 20220213.pkl')
    pegas = ext.load()
    ext.save(pegas, 'just a test.pkl')


        
   
    






        







