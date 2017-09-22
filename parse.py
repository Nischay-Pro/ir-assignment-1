import json
import os
import errno
import nltk
import newspaper
import pymysql.cursors
from newspaper import ArticleException
nltk.download('punkt')

def main():
    with open('config.json', 'r') as f:
        ARR = json.load(f)
    HOST = (ARR)['db-host']
    USER = (ARR)['db-username']
    PASSWORD = (ARR)['db-password']
    DBNAME = (ARR)['db-name']

    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DBNAME, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    try:
        SITEARRAY = ["www.wired.com", "www.theverge.com","www.extremetech.com"]
        for webitem in SITEARRAY:
            newsitem = newspaper.build("http://" + webitem, memoize_articles = False)
            for articleitem in newsitem.articles:
                try:
                    os.makedirs("irdata")
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
                print(articleitem.url)
                try:
                    articleitem.download()
                    articleitem.parse()
                except ArticleException:
                    pass
                with connection.cursor() as cursor:
        # Read a single record
                    sql = "SELECT LAST_INSERT_ID(uid) From ir_articles ORDER BY uid DESC LIMIT 1"
                    cursor.execute(sql, )
                    result = cursor.fetchone()
                    if result != None:
                        uid = result['LAST_INSERT_ID(uid)'] + 1
                    else:
                        uid = 1
                with connection.cursor() as cursor:
                    # print("irdata/" + str(uid) + ".txt")
                    file = open("irdata/" + str(uid) + ".txt", "w", encoding="utf-8")
                    file.write(articleitem.text.encode('utf-8', 'ignore').decode('utf-8'))
                    file.close()
                    sql = "INSERT INTO `ir_articles` (`url`, `text`, `title`) VALUES (%s, %s, %s)"
                    # print(articleitem.url, articleitem.text, articleitem.title)
                    cursor.execute(sql, (articleitem.url, "irdata/" + str(uid) + ".txt", articleitem.title))
                connection.commit()
            
        # selected = newsitem.articles[10]
        # print(selected.url)
        # downloaded=newsitem.articles[10]
        # downloaded.download()
        # downloaded.parse()
        # #print(downloaded.text)
        # downloaded.nlp()
        # print(downloaded.summary)
    finally:
        connection.close()
if __name__ == "__main__":
    main()