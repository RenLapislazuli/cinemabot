import asyncio
from cinemabot import dependencies
# from urllib.parse import urljoin

import aiohttp

async def main():
#     settings = dependencies.get_settings()
#     api_key = settings.google.api_key
#     search_key = settings.google.search_engine_id
#     session = aiohttp.ClientSession()
#     async with session.get(
#         "https://www.googleapis.com/customsearch/v1",
#         params = {
#             "q": "Frieren смотреть",
#             "cx": search_key,
#             "key": api_key,
#         },
#         ) as response:
#         print(response)
    client = dependencies.get_google_client()
    # film_info = await client.get_film_details(5401195)
    # print(film_info["name"])
    # print(film_info["description"])
    # print(film_info["rating"]["kp"])
    resp = await client.search_google("Frieren смотреть")
    print(resp["items"][0]["link"])

asyncio.run(main())
