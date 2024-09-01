import scrapy
from scrapy import Request
from scrapy_playwright.page import PageMethod
from Scrape_Periodic_Table.items import PeriodicTableItem
from itemloaders import ItemLoader


class ElementsSpiderSpider(scrapy.Spider):
    name = "elements_spider"
    allowed_domains = ["nih.gov"]
    start_urls = ["https://pubchem.ncbi.nlm.nih.gov/ptable/"]
    elements = []

    def start_requests(self):
        yield Request(self.start_urls[0],
                            meta=dict(
                            playwright= True,
                            playwright_page_methods=[
                                PageMethod('wait_for_load_state',"domcontentloaded"),
                                PageMethod('wait_for_function', "document.querySelector('div.element div[data-tooltip=\"Symbol\"]') !== null")
                                ]
                        ))

    def parse(self, response):
        for element in response.css('div.element'):
            item_loader = ItemLoader(item=PeriodicTableItem(), selector=element)
            
            item_loader.add_css('symbol', 'div[data-tooltip="Symbol"]')
            item_loader.add_css('name', 'div[data-tooltip="Name"]')
            item_loader.add_css('atomic_mass', 'div[data-tooltip*="Atomic Mass"]')
            item_loader.add_css('atomic_number', 'div[data-tooltip="Atomic Number"]')
            item_loader.add_css('chemical_group', 'div[data-tooltip="Chemical Group Block"] span')

            yield item_loader.load_item()
