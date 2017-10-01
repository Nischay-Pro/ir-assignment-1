import nltk
import individual_file
import experiment
from operator import itemgetter

query = "adding airline among"

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
query_dictionary = {}
for word in query_term_freq:
    answer = []
    query_dictionary[word[0]] = experiment.vocabulary[word[0]]
    for item in query_dictionary[word[0]]:
        answer = answer + [[item[0], item[1]*word[1]]]
    query_dictionary[word[0]] = answer


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
for index in range(1, 11):
    print(index, ":", final_list[index][0])

