# Scrape Periodic table elements

![Periodic table website](<screenshots/Screenshot from 2024-08-31 11-43-19.png>)

## About 

* A python script that scrapes elements info from [Periodic table website](https://pubchem.ncbi.nlm.nih.gov/ptable/ "Periodic table website"), then

* Extracts the following info of each element:
    * symbol
    * name
    * atomic mass
    * atomic number
    * chemical group

* Store the info in a table in a Sqlite database as follows:
![periodic_table.db](<screenshots/Screenshot from 2024-08-31 11-48-50.png>)

* Output the info to a json file organized by chemical group as follows:
![result.json](<screenshots/Screenshot from 2024-08-31 11-55-14.png>)
      
## Libraries Used
* Scrapy
* Playwright
* Sqlite3


## Installing

#### Download the code from Github
#### Open CLI and Go to the project folder
#### Run the following command

```
pip install -r requirements.txt
```

## Running
#### Run the following command:

```
scrapy crawl elements_spider
```

