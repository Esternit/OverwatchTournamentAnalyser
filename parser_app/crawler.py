import asyncio
import aiohttp
from bs4 import BeautifulSoup

from data.config import config

class AnakCrawler:
    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }
    
    async def fetch_main(self):

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(config.TOURNAMENTS_URL) as response:

                    html = await response.text()
                    return html

    async def fetch_matches_page(self, number, page):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(config.TOURNAMENTS_URL + str(number) + "?tab=matches&search=&page=" + str(page)) as response:
                
                    html = await response.text()
                    return html
    
    async def fetch_match_page(self, number):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(config.MATCH_URL + str(number)) as response:
                
                    html = await response.text()
                    return html
