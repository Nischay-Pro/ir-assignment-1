import json
import sys
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
    MEMOIZE = (ARR)['memoize']
    SOURCES = (ARR)['sources']

    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DBNAME, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    print("Database Connection Established")
    if len(SOURCES) != 0:
        print("Warning! " + str(len(SOURCES)) + " custom source(s) has been added. Parsing may fail.")
    try:
        SITEARRAY = ["https://www.wired.com","https://www.theverge.com","https://www.extremetech.com"]
        for urlitem in SOURCES:
            SITEARRAY.append(urlitem)
        for webitem in SITEARRAY:
            print("Parsing from: " + webitem)
            newsitem = newspaper.build(webitem, memoize_articles = MEMOIZE)
            count = 0
            print("Found " + str(len(newsitem.articles)) + " new articles!")
            for articleitem in newsitem.articles:
                with connection.cursor() as cursor:
                    sql = "SELECT * From ir_articles WHERE url='" + articleitem.url + "'"
                    cursor.execute(sql, )
                    result = cursor.fetchone()
                    if result == None and not articleitem.url.endswith('#comments'):
                        progress(count,len(newsitem.articles), str(str(count) + "/" + str(len(newsitem.articles))))
                        try:
                            os.makedirs("irdata")
                        except OSError as e:
                            if e.errno != errno.EEXIST:
                                raise
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
                            title = articleitem.title
                            if title == None:
                                title = "No Title"
                            cursor.execute(sql, (articleitem.url, "irdata/" + str(uid) + ".txt", title))
                        connection.commit()

                    count += 1
            cleanandoutput("Parsed successfully from: " + webitem)
            
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
def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total))
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()

def cleanandoutput(message):
    sys.stdout.write("\n" + message)
    print("")
if __name__ == "__main__":
    main()