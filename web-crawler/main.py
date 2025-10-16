from crawler import AsyncCrawler;
from indexer import indexer;

if __name__ == "__main__":
    import asyncio

    async def main():
        crawler = AsyncCrawler(max_concurrency=5)
        my_indexer = indexer()
        
        urls = [
            "https://example.com",
            "https://www.python.org",
            "https://docs.aiohttp.org",
            "https://www.geeksforgeeks.org/",
        ]
        results = await crawler.crawl(urls)
        URL_counter = 0
        
        for page in results:
            if page:
                page_text = page.title
                for header in page.headers:
                    page_text += " " + header.lower()
                    
                my_indexer.add_page(page.url, page_text)
                # print(f"\nURL #{URL_counter}: {page.url}")
                # print(f"Title: {page.title}")
                # print(f"H1s: {page.headers}")
                # print(f"Links found: {len(page.links)}")
            URL_counter += 1
        
        query = input("Enter a word to search: ").lower()
        
        print(f"Search for {query}")
        
        results = my_indexer.search(query)
        if results:
            for url, count in results:
                print(f"{url} → {count}")
        else:
            print("No results found.")
        
        # print("Response: \n", my_indexer.inverted_index.get(search_word))
        
        # tokenized_words = my_indexer.tokenize("Python is great for asynchronous programming!")
        # print(tokenized_words)
        
        # my_indexer.add_page("https://example.com", "Python is great. Python is fun. asynchronous asynchronous asynchronous")
        # my_indexer.add_page("https://docs.aiohttp.org", "Python is great for asynchronous PyThOn programming!")
        # my_indexer.add_page("https://www.python.org", "Some random words for dictionary.")
        # print(my_indexer.inverted_index)
        
    asyncio.run(main())
