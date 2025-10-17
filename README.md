# Async Web Crawler

## Overview

**Async Web Crawler** is a lightweight Python project that crawls websites asynchronously, indexes page content, and allows keyword or phrase searches across the indexed pages.
It demonstrates core concepts in **asynchronous programming, web scraping, and information retrieval**, giving you a hands-on mini search engine experience.

---

## Features

* **Asynchronous Crawling** — Fetch multiple pages concurrently using `aiohttp` and `asyncio`.
* **HTML Parsing** — Extract page titles, headers, and links with `BeautifulSoup`.
* **Inverted Index** — Efficiently maps words to URLs and counts occurrences.
* **Tokenization & Stopword Filtering** — Clean and normalize text for indexing.
* **Multi-word Search Queries** — Rank results by frequency across all query terms.
* **Modular Design** — Organized into `crawler.py`, `indexer.py`, and `main.py`.

---

## How It Works

1. `AsyncCrawler` fetches pages from a list of URLs asynchronously.
2. `Indexer` processes page text (titles + headers) and updates the inverted index.
3. The user inputs a query; the search function returns top URLs ranked by word frequency.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/benjaminburnell/async-web-crawler
cd async-web-crawler
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the main program

```bash
python main.py
```

You will be prompted to enter a search query after crawling:

```
Enter a word or phrase to search: python async
```

---

## Built With

* **Python 3.x** — core language for crawling, indexing, and searching
* **aiohttp & asyncio** — asynchronous HTTP requests
* **BeautifulSoup4** — parsing HTML content
* **Dataclasses & Typing** — structured and type-annotated code
* **Collections** — efficient frequency counting for inverted index

---

## Future Enhancements

* Implement **exact phrase search** and **fuzzy search**.
* Persist the inverted index using **SQLite** or **pickle** to avoid re-crawling pages.
* Add a **CLI or web interface** for live search queries.
* Enhance **tokenization** with stemming and lemmatization for better word matching.
* Enable **automatic crawling of internal links** to index entire websites.

---

## License

MIT License © 2025 Benjamin Burnell

You’re free to use, modify, and distribute this project under the terms of the MIT License.

---

## Credits

Developed by **Benjamin Burnell**  
Powered by **aiohttp**, **BeautifulSoup4**, and Python’s standard libraries.
