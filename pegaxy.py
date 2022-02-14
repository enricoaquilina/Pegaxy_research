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

        self.url1 = ""
        self.url2 = ""
        self.url3 = ""
        
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
        r = requests.get("https://api-apollo.pegaxy.io/v1/game-api/market/pegasListing/{id}?&marketType=FixedPrice&currency=0xc2132D05D31c914a87C6611C10748AEb04B58e8F&breedFrom=0&breedTo=7")
        print("Getting {} Pegas, {} pages".format(r.json()['total'], math.ceil(r.json()['total'] / 12)))
        return math.ceil(r.json()['total'] / 12)
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

# Start Extraction
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(ext.start(ext.get_count()))
    asyncio.run(ext.get_deets())

    
# Start Transformation
    ## pegas = [pega['nft']['win_rate'] = "{:.4f}".format(win_rate * 100) for pega in pegas if 'nft' in pega]
    
    # pegas = ext.load('all_pegas 20220213.pkl')
    pegas = ext.load()
    # for pega in pegas:
    #     if 'message' not in pega:
    #         if 'nft' in pega and 'total_races' in pega['nft'] and pega['nft']['total_races'] != 0:
    #             win_rate = pega['nft']['win'] / pega['nft']['total_races']
    #             pega['win_rate'] = win_rate * 100
    #             # pega['win_rate'] = "{:.4f}".format(win_rate * 100)
    #         if 'price' in pega['listing']:
    #             pega['price'] = int(pega['listing']['price'])/1000000
    #         if  pega['nft']['speed'] > 0 and pega['nft']['strength'] > 0 and pega['nft']['wind'] > 0 and \
    #             pega['nft']['water'] > 0 and pega['nft']['fire'] > 0 and pega['nft']['lighting'] > 0:
    #             pega['all_stats_mean'] = statistics.fmean([pega['nft']['speed'], pega['nft']['strength'], pega['nft']['wind'], pega['nft']['water'], pega['nft']['fire'], pega['nft']['lighting']])
    #             pega['rng_mean'] = statistics.fmean([pega['nft']['wind'], pega['nft']['water'], pega['nft']['fire'], pega['nft']['lighting']])



    # df = pd.DataFrame(pegas)
    # # Slice dataframe to get separate win rates (20%-30%, 30%-40%, 40%-50%, 50-60%)
    # # Compute mean stats value
    # df['win_rate'] = df['win_rate'].replace(np.nan, 0)
    # df['price'] = df['price'].replace(np.nan, 0)
    # df = df.sort_values(by=['win_rate'], ascending=False)


    # win_rate1 = df[df['win_rate'] > 19]
    # win_rate2 = df[(df['win_rate'] > 19) & (df['win_rate'] <= 30)]
    # win_rate3 = df[(df['win_rate'] > 30) & (df['win_rate'] <= 40)]
    # win_rate4 = df[(df['win_rate'] > 40) & (df['win_rate'] <= 50)]
    # win_rate5 = df[df['win_rate'] > 50]
    
    # test = df[df['price'] <= 3000]
    # test = test.sort_values(by=['win_rate'], ascending=False).head(20) 
    # # print(test)

    # plt.scatter(win_rate1['win_rate'], win_rate1['price'])
    # plt.show()

    # plt.scatter(win_rate2['win_rate'], win_rate2['price'])
    # plt.show()

    # plt.scatter(win_rate3['win_rate'], win_rate3['price'])
    # plt.show()

    # plt.scatter(win_rate4['win_rate'], win_rate4['price'])
    # plt.show()

    # plt.scatter(win_rate5['win_rate'], win_rate5['price'])
    # plt.show()


    # # plt.scatter(test['stats_mean'], test['win_rate'])
    # # plt.show()
    
    
    # # plt.scatter(test['price'], test['all_stats_mean'])
    # # plt.show()

    # plt.scatter(test['price'], test['rng_mean'])
    # plt.show()

    ext.save(pegas, 'just a test.pkl')
    






        







