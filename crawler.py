# crawler.py

# Import needed libraries
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dataclasses import dataclass
from typing import List, Optional
import logging

@dataclass

# Data structure for the data that the AsyncCrawler will return to the main function
class PageData:
    
    ###
    # url will have a type of str(String)
    url: str
    
    ### 
    # title will have a type of str(String) this is optional as it could contain no data or value
    title: Optional[str]
    
    ###
    # headers will have a type of List[str] this will return a list of strings that 
    # are the headers of the page inside the AsyncCrawler it specifically only looks 
    # for <h1> elemenets in the html.
    headers: List[str]
    
    ### 
    # links will have a type of List[str] this like headers will return a list of strings but 
    # it will be specifically for links we get this through the html element 
    # <a> we also make sure later on that the element has a href=true which means a link 
    # is attached.
    links: List[str]

# Creating the AsyncCrawler class
class AsyncCrawler:
    
    ### 
    # Initialize the varaibles we are going to use for the object AsyncCrawler
    def __init__(self, max_concurrency: int = 10, timeout: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.logger = logging.getLogger(__name__)

    ### 
    # fetch is an async function that will get the HTML content of a page
    # it uses a semaphore to make sure we don't fetch too many pages at once
    # it takes in a session (aiohttp.ClientSession) and a url (string)
    # it returns the HTML as a string if successful, or None if there was an error
    async def fetch(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        async with self.semaphore:  # make sure we respect the max concurrency limit
            try:
                async with session.get(url) as resp:  # send a GET request to the url
                    if resp.status != 200:  # check if the response is not "OK"
                        self.logger.warning(f"Non-200 response for {url}: {resp.status}")  # log a warning
                        return None  # return nothing if page couldn't be fetched successfully
                    return await resp.text()  # return the HTML content as a string
            except aiohttp.ClientError as e:  # handle common network errors
                self.logger.error(f"Failed to fetch {url}: {e}")  # log the error
                return None  # return nothing if there was a network error

    ### 
    # parse is a function that will take HTML content and extract data from it
    # it takes in the url of the page and the HTML as a string
    # it returns a PageData object containing the URL, title, headers, and links
    def parse(self, url: str, html: str) -> PageData:
        soup = BeautifulSoup(html, "html.parser")  # create a BeautifulSoup object to parse HTML
        title = soup.title.string if soup.title else None  # get the page title, or None if missing
        headers = [h.get_text(strip=True) for h in soup.find_all("h1")]  # get all <h1> headers as text
        links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]  # get all <a> links with href and make them absolute URLs
        return PageData(url, title, headers, links)  # create and return a PageData object with the extracted info

    ### 
    # crawl is an async function that will take a list of URLs and fetch them all
    # it uses fetch_and_parse to get the HTML and convert it to PageData
    # it returns a list of PageData objects (or None if a page failed to fetch)
    async def crawl(self, urls: List[str]) -> List[PageData]:
        async with aiohttp.ClientSession(timeout=self.timeout) as session:  # create a session for all requests
            tasks = [self.fetch_and_parse(session, url) for url in urls]  # create a list of tasks to fetch and parse each URL
            return await asyncio.gather(*tasks)  # run all tasks concurrently and gather results

    ### 
    # fetch_and_parse is an async function that combines fetching and parsing for a single URL
    # it first calls fetch to get the HTML
    # if HTML was fetched successfully, it calls parse to extract the data
    # it returns a PageData object or None if fetching failed
    async def fetch_and_parse(self, session: aiohttp.ClientSession, url: str) -> Optional[PageData]:
        html = await self.fetch(session, url)  # fetch the page HTML
        if html:  # if HTML exists (was fetched successfully)
            return self.parse(url, html)  # parse the HTML and return PageData
        return None  # return nothing if fetch failed