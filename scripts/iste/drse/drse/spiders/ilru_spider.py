"""
# ilru_spider.py
# @author Ian Effendi
#
# Spider for reading ILRU pages.
"""
from bs4 import BeautifulSoup

import scrapy

def get_cils(response):
    content = BeautifulSoup(response.text, 'lxml')
    return content.find_all("div", class_="cil-block"), content
class ILRUSpider(scrapy.Spider):
    name = "ilru"
    help = "scrapy crawl ilru -a [STATE]"
    
    def __init__(self, state='NY', **kwargs):
        self.state = state
        self.start_urls = [ f'https://www.ilru.org/projects/cil-net/cil-center-and-association-directory-results/{state}' ]
        super().__init__(**kwargs)
        
    def parse(self, response):
        # page = response.url.split("/")[-2]
        filename = f'ilru-{self.state}-results.html'
        cils, soup = get_cils(response)
        with open(filename, 'w') as f:
            for cil in cils:
                f.write(('=' * 10) + '\n' + cil.prettify())
        self.log(f'Saved file {filename}')
        
        
        # Selectors:
        # response.css('#block-system-main').xpath('.//div').