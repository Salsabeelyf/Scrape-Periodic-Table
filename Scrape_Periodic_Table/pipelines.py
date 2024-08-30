# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import sqlite3
from itemadapter import ItemAdapter


class ScrapePeriodicTablePipeline:
    def process_item(self, item, spider):
        return item


class SaveToDatabasePipeline:
    def __init__(self):
        self.con = sqlite3.connect('periodic_table.db')
        self.cur = self.con.cursor()

    def open_spider(self, spider):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS periodic_table
                         (element_symbol TEXT PRIMARY KEY,
                         element_name TEXT,
                         atomic_number INTEGER,
                         atomic_mass REAL,
                         chemical_group TEXT)
                         """)
        self.con.commit()

    def process_item(self, item, spider):
        self.con.execute("""
                             INSERT INTO periodic_table (element_symbol, element_name, atomic_number, atomic_mass, chemical_group) VALUES (?,?,?,?,?)""",
                             (item['symbol'], item['name'], item['atomic_number'], item['atomic_mass'], item['chemical_group']))
        self.con.commit()
        return item

    def close_spider(self, spider):
        self.con.close()


class SaveToJsonPipeline:
    def process_item(self, item: dict, spider):  # default method
        # calling dumps to create json data.
        line = json.dumps(dict(item)) + "\n"
        # converting item to dict above, since dumps only intakes dict.
        self.file.write(line)                    # writing content in output file.
        return item
 
    def open_spider(self, spider):
        self.file = open('result.json', 'w')
 
    def close_spider(self, spider):
        self.file.close()