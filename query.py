import nltk
import individual_file
import json
import sys
import pymysql.cursors
from operator import itemgetter

def main(query):
    if query==None:
        query = input("Enter your query: ")
    # query term frequency
    tokens = individual_file.get_tokens(query)
    stop_tokens = individual_file.remove_stop_words(tokens)
    lemma_tokens = individual_file.normalization(stop_tokens)
    lemma_tokens.sort()
    freq = nltk.FreqDist(lemma_tokens)
    query_term_freq = []
    for key, val in freq.items():
        query_term_freq = query_term_freq + [[str(key), val]]

    # Multiplying term frequency with query frequency
    with open('invertedindex.json', 'r', encoding="utf-8") as f:
        try:
            data = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            data = {}
    query_dictionary = {}
    try:
        for word in query_term_freq:
            answer = []
            query_dictionary[word[0]] = data[word[0]]
            for item in query_dictionary[word[0]]:
                answer = answer + [[item[0], item[1]*word[1]]]
            query_dictionary[word[0]] = answer
    except KeyError:
        query_dictionary = {}

    # Ranked function in the form of dictionary
    ranked_list = {}
    for word in query_dictionary:
        for item in query_dictionary[word]:
                try:
                    ranked_list[item[0]] += item[1]
                except:
                    ranked_list[item[0]] = item[1]


    # ranked list as list of lists
    final_list = []
    for k, v in ranked_list.items():
        final_list.append([k, v])
    final_list.sort(key=itemgetter(1), reverse=True)


    # Result to the Query
    with open('config.json', 'r') as f:
        ARR = json.load(f)
    HOST = (ARR)['db-host']
    USER = (ARR)['db-username']
    PASSWORD = (ARR)['db-password']
    DBNAME = (ARR)['db-name']
    MEMOIZE = (ARR)['memoize']

    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DBNAME, charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    print("Found " + str(len(final_list)) + " results. Displaying top " + str(min(10, len(final_list) - 1)))
    for index in range(1,min(11,len(final_list))):
        print("Article " + str(index) + ":")
        with connection.cursor() as cursor:
            sql = "SELECT title From ir_articles WHERE uid=" + str(final_list[index][0]) + ""
            cursor.execute(sql, )
            result = cursor.fetchone()
            r = json.dumps(result)
            ARR = json.loads(r)
            title = (ARR)['title']
        print("Article Title: " + str(title))
        print("File Path: " + "irdata\\" + str(final_list[index][0]) + ".txt")

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        main(None)