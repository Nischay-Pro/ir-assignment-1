# General Installation

1. Install [python 3.6](https://www.python.org/downloads) (or greater) **(Required)**
2. Install MariaDB or MySQL DB for configuring quick cache database **(Required)**
3. Install phpMyAdmin and Apache for using GUI based Database Management (Optional)

## Packages required to be installed

- nltk
- json
- pymysql
- newspaper
- matplotlib
- numpy
- networkx
- scipy
- sklearn
- timeit

Install using pip3 by entering the following command

    > pip3 install nltk
    > pip3 install json
    > pip3 install pymysql
    > pip3 install newspaper3k


## Configuring your Quick Cache Database

### Importing SQL File
This project uses a quick cache database to support parsing and indexing resumability. This allows the user to automatically update their dataset (WITH NEW ADDITIONS) without the need to download the entire dataset again.

The project directory contains a folder called  ***schema***

1. Navigate to ***schema***
2. Import the ***ir.sql*** file using PhpMyAdmin or the native MySQL DB sql importing tool.

*Note:* The sql file imported automatically generates the database with the following structure

    databases
    --> ir 
    tables
        ir_articles
                    --> uid     (INT)
                    --> url     (TEXT)
                    --> text    (TEXT)
                    --> title   (TEXT)
                    --> indexed (TINYINT)
                    --> backlinks (TEXT)
                    --> inlinks (TEXT)
                    --> pagerank (TEXT)


### Configuring config.json

In your project directory there exists a config.json
- ``db-username`` is your database username. Default is **root**
- ``db-password`` is your database password. Default is *null*
- ``db-name`` is your quick cache database name. Default is **ir**
- ``db-host`` is your database host. Default is **localhost**

Edit your json file accordingly with the changes you made.

Run ***check_connections.py*** in project root folder to check if connections are working

    > python check_connections.py
    > success

If you do not get the following message. Please check if you have installed all the packages and configured the database properly.

# General Usage and Instructions

## parse.py
    Running Instructions
    > python parse.py
    
The python script *parse.py* is used to retrieve articles from several technology related websites.
The parsing is done using Natural Language Processing by automatically extracting meaningful news posts from websites.
- The script automatically detects article posts from the web news homepage without any need of human interaction.
- All new articles are scrapped and stored in a text file and meta data of the article is stored in the database.
- By default articles from the following websites are extracted
    1. [Wired](https://www.wired.com)
    2. [The Verge](https://www.theverge.com)
    3. [Extreme Tech](https://www.extremetech.com)

### Configuring parse.py to extract articles from websites other than the default

parse.py is capable of extracting from news websites other than the articles specified. However be warned there is no guarantee articles will be extracted successfully.

To add a website to scrap articles from

1. Under the project root folder open config.json
2. In sources enter the website url (Homepage) you want to scrap from.

        For Example
        {
        "memoize":false,
        "db-username":"root",
        "db-password":"",
        "db-name":"ir",
        "db-host":"localhost",
        "sources":["http://www.website1.com"] // In case you have 1 website
        }
        For 2 or more websites
        {
        "memoize":false,
        "db-username":"root",
        "db-password":"",
        "db-name":"ir",
        "db-host":"localhost",
        "sources":["http://www.website1.com","http://www.website2.com","http://www.website3.com"] // Each website is separated by a comma
        }

Save and run the parser.

## Generating the invertedindex.py

Run invertedindex.py to automatically generate the inverted index for the articles extracted. 
Files already indexed will not be indexed again.

## Running a query

Run query.py and type in a query. The top 10 (or available articles) will be shown in decreasing order of ranking.