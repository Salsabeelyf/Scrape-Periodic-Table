import scrapy
from scrapy import Request
from scrapy_playwright.page import PageMethod


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
        for e in response.css('div.element'):
            yield{
                "symbol": e.css('div[data-tooltip="Symbol"]::text').get(),
                "name": e.css('div[data-tooltip="Name"]::text').get(),
                "atomic_mass": float(e.css('div[data-tooltip="Atomic Mass, u"]::text').get()),
                "atomic_number": int(e.css('div[data-tooltip="Atomic Number"]::text').get()),
                "chemical_group": e.css('div[data-tooltip="Chemical Group Block"] span::text').get()
            }



# Exctract:
# symbol div[data-tooltip="Symbol"]::text
# name div[data-tooltip="Name"]::text
# atomic mass (float) div[data-tooltip="Atomic Mass, u"]::text
# atomic number (int)  div[data-tooltip="Atomic Number"]::text
# chemical group div[data-tooltip="Chemical Group Block"] span::text


# Save data into database

# output data as a nested dictionary grouped by chemical group
# {
#     "nonmetal": {
#         "element_count": 7,
#         "elements": [
#             {
#                 "symbol": "H",
#                 "name": "Hydrogen",
#                 "atomic_number": 1,
#                 "atomic_mass": 1.008
#             },
#             {
#                 "symbol": "H",
#                 "name": "Hydrogen",
#                 "atomic_number": 1,
#                 "atomic_mass": 1.008
#             }
#         ]
#     }
# }