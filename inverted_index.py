import individual_file
import json
import sys
import os
import pymysql.cursors
from operator import itemgetter
import json

def main():
    with open('config.json', 'r') as f:
        ARR = json.load(f)
    HOST = (ARR)['db-host']
    USER = (ARR)['db-username']
    PASSWORD = (ARR)['db-password']
    DBNAME = (ARR)['db-name']
    MEMOIZE = (ARR)['memoize']

    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DBNAME, charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    try:
        doc_id = 1
        sorted_dictionary = []
        with connection.cursor() as cursor:
            sql = "SELECT text,uid From ir_articles WHERE indexed='0'"
            cursor.execute(sql, )
            result = cursor.fetchall()
            print("Generating Inverted Index for " + str(len(result)) + " unindexed files.")
        # sorted_dictionary contains the list of lists with with each list containing the information [word,doc_id,term_freq]
        count = 0
        for file in result:
            r = json.dumps(file)
            ARR2 = json.loads(r)
            file_name = (ARR2)['text']
            doc_id = (ARR2)['uid']
            if file_name.endswith(".txt"):
                f = open(file_name,'r', encoding="utf-8")
                text = f.read()
                sorted_dictionary = sorted_dictionary + individual_file.get_term_frequencies(text, doc_id)
                count+=1
                progress(count,len(result)," Generating Sorted Dictionary")
                f.close()
        sorted_dictionary.sort(key=itemgetter(0))
        cleanandoutput("Generated Sorted Dictionary")

        # Dictionary with postings is stored in vocabulary
        vocabulary = {}
        present_word = " "
        word_count = 0
        for word in sorted_dictionary:
            progress(word_count,len(sorted_dictionary)," Generating Vocabulary List")
            if word[0] == present_word:
                vocabulary[word[0]] += [[word[1],word[2]]]
            else:
                present_word = word[0]
                vocabulary[word[0]] = [[word[1],word[2]]]
            word_count += 1


        # sorting the postings of a particular word
            for key in vocabulary:
                vocabulary[key].sort(key=itemgetter(0))
        try:
            with open('invertedindex.json', 'r', encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except ValueError:
                    data = {}
        except FileNotFoundError:
            open('invertedindex.json', 'w', encoding="utf-8")
            data = {}
        data2 = dict(vocabulary, **data)
        # save to file:
        with open('invertedindex.json', 'w', encoding="utf-8") as f:
            json.dump(data2, f)
        with connection.cursor() as cursor:
            sql = "UPDATE `ir_articles` SET indexed=1 WHERE indexed=0;"
            cursor.execute(sql, )
        connection.commit()
        cleanandoutput("Generated Inverted Index")
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