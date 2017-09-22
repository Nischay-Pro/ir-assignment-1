import requests
from bs4 import BeautifulSoup
import json
import nltk
nltk.download('popular')

# with open('config.json', 'r') as f:
#     array = json.load(f)
# depth=(array)['depth']
# print(depth)
import newspaper

paper = newspaper.build('http://www.gizmodo.in/software',memoize_articles=False)
selected=paper.articles[10]
print(selected.url)
downloaded=paper.articles[10]
downloaded.download()
downloaded.parse()
#print(downloaded.text)
downloaded.nlp()
print(downloaded.summary)