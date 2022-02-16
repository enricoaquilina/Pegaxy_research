# async def get_pegas(session, page, url):
#     try:
#         url = "https://api-apollo.pegaxy.io/v1/game-api/market/pegasListing/page={}&marketType=FixedPrice&currency=0xc2132D05D31c914a87C6611C10748AEb04B58e8F&breedFrom=0&breedTo=7".format(page)

#         response = await session.request(method='GET', url=url)
#         response.raise_for_status()

#         print(f"Response status ({url}): {response.status}")

#     except HTTPError as http:
#         print("Http Error: {}".format(http))
#     except Exception as err:
#         print("An error occurred: {}".format(err))

#     response_json = await response.json()
#     return response_json



    # pega_processed = []
    # with alive_bar(len(pega_details), bar = 'bubbles', spinner = 'notes2') as bar:
    #     for id, horse in enumerate(pega_details):
    #         header = {
    #             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    #             "Accept-Encoding": "gzip, deflate", 
    #             "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", 
    #             "Dnt": "1", 
    #             # "Host": "httpbin.org", 
    #             "Upgrade-Insecure-Requests": "1", 
    #             "User-Agent": random.choice(user_agent_list) 
    #         }
    #         deets_url = "https://api.pegaxy.io/market/listing/{id}".format(id=horse['id'])

    #         pega_info = requests.get(deets_url, headers=header)
            
    #         pega_processed.append(pega_info.json())
            

    # starttime = timeit.default_timer()
    # print("Extracted {} Pegas for {}".format(len(pega_processed), datetime.now().strftime("%Y%m%d")))