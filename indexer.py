# indexer.py

# Import needed libraries
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dataclasses import dataclass
from typing import List, Optional
import logging
import string


class indexer():
    def __init__(self):
        self.inverted_index = {}
        self.stopwords = ["is", "for", "as", "to", "all", "the", "your", "you"]
        
    def tokenize(self, text: str) -> List[str]:
        text = text.strip(string.punctuation)
        words = [ ''.join(c for c in word if c.isalpha()).lower() 
                for word in text.split() 
                if ''.join(c for c in word if c.isalpha()).lower() not in self.stopwords ]
        return words

    def add_page(self, URL: str, text: str) -> None:
        words = self.tokenize(text)
        
        for word in words:
            if word in self.inverted_index:  # if the word is already in the dictionary
                if URL in self.inverted_index[word]:
                    self.inverted_index[word][URL] = self.inverted_index[word][URL] + 1  # increase its count by 1
                else:
                    self.inverted_index[word][URL] = 1  # otherwise, add it to the dictionary with count 1
            else:
                self.inverted_index[word] = {URL: 1}  # otherwise, add it to the dictionary with count 1
                
    def search(self, query: str, top_k: int = 10):
        # Tokenize the query like you do for pages
        query_words = [word.lower() for word in query.split() if word.lower() not in self.stopwords]
        
        # Dictionary to accumulate total frequency per URL
        url_scores = {}
        
        for word in query_words:
            urls = self.inverted_index.get(word, {})
            for url, count in urls.items():
                url_scores[url] = url_scores.get(url, 0) + count
        
        # Sort URLs by total frequency descending
        sorted_results = sorted(url_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return top_k results
        return sorted_results[:top_k]

