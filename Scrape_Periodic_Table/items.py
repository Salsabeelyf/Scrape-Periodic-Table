import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


class PeriodicTableItem(scrapy.Item):
    name = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    symbol = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    atomic_mass = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, float),
        output_processor = TakeFirst()
    )
    atomic_number = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, int),
        output_processor = TakeFirst()
    )
    chemical_group = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
