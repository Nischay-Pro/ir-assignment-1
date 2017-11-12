import os
import sys
import copy
import collections
import json
import nltk
import nltk.tokenize
import pymysql.cursors
import urllib.request
from bs4 import BeautifulSoup
import lxml.html
import networkx as nx
import matplotlib.pyplot as plt

def main():
    with open('./../config.json', 'r') as f:
        ARR = json.load(f)
    HOST = (ARR)['db-host']
    USER = (ARR)['db-username']
    PASSWORD = (ARR)['db-password']
    DBNAME = (ARR)['db-name']
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DBNAME, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = "SELECT uid,url From ir_articles"
        cursor.execute(sql, )
        result = cursor.fetchall()
    urlslist = []
    for querydata in result:
        urlslist.append(querydata['url'])
    val = 1
    for urls in urlslist:
        resp = urllib.request.urlopen(urls)
        soup = BeautifulSoup(resp, from_encoding=resp.headers.get_content_charset(failobj="utf-8"))
        index = []
        for link in soup.find_all('a', href=True):
            index = index + [i for i, s in enumerate(urlslist) if link['href'] in s]
        index = (list(set(index)))
        index = [x+1 for x in index]
        with connection.cursor() as cursor:
            backlinks = (str(index))
            backlinks = str(backlinks.replace('[','').replace(',','').replace(']',''))
            sql = "UPDATE `ir_articles` SET `backlinks`='" + backlinks + "' WHERE uid=" + str(val)
            cursor.execute(sql)
        connection.commit()
        val += 1
        with connection.cursor() as cursor:
            sql = "SELECT LAST_INSERT_ID(uid) From ir_articles ORDER BY uid DESC LIMIT 1"
            cursor.execute(sql, )
            result = cursor.fetchone()
            if result != None:
                uid = result['LAST_INSERT_ID(uid)'] + 1
            else:
                uid = 1
        for i in range(1, uid+1, 1):
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `ir_articles` WHERE backlinks LIKE '% " + str(i) + " %' OR backlinks LIKE '% " + str(i) + "' OR backlinks LIKE '" + str(i) + " %'"
                cursor.execute(sql, )
                result = cursor.fetchall()
            inlinks = []
            for item in result:
                inlinks.append(item['uid'])
            with connection.cursor() as cursor:
                inlinks = str(inlinks)
                inlinks = inlinks.replace('[','').replace(',','').replace(']','')
                sql = "UPDATE `ir_articles` SET `inlinks`='" + inlinks + "' WHERE uid=" + str(i)
                cursor.execute(sql)
            connection.commit()
#SELECT * FROM `ir_articles` WHERE backlinks LIKE '% 2 %' OR backlinks LIKE '% 2' OR backlinks LIKE '2 %'
if __name__ == "__main__":
    main()