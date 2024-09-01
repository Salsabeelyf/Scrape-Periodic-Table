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
    elements = {}
    keys_to_extract = ["symbol", "name", "atomic_mass", "atomic_number"]

    def process_item(self, item, spider):  # default method
        chemical_group = item["chemical_group"]
        if chemical_group not in self.elements.keys():
            self.elements[chemical_group] = {
                "element_count": 0,
                "elements": []
            }
        self.elements[chemical_group]["element_count"] += 1
        self.elements[chemical_group]["elements"].append({key: item[key] for key in self.keys_to_extract})
        return item
 
    def open_spider(self, spider):
        self.file = open("result.json", "w")
 
    def close_spider(self, spider):
        self.file.write(json.dumps(dict(self.elements)))
        self.file.close()