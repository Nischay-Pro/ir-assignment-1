import individual_file
import os
from operator import itemgetter

doc_id = 1
sorted_dictionary = []

# sorted_dictionary contains the list of lists with with each list containing the information [word,doc_id,term_freq]
directory = os.path.normpath("C:/Users/sumeeth/Desktop/dataset/TOI/business")
for subdir, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".txt"):
             f = open(os.path.join(subdir ,file),'r')
             text = f.read()
             sorted_dictionary = sorted_dictionary + individual_file.get_term_frequencies(text, doc_id)
             doc_id += 1
             f.close()
sorted_dictionary.sort(key=itemgetter(0))


# Dictionary with postings is stored in vocabulary
vocabulary = {}
present_word = " "
for word in sorted_dictionary:
    if word[0] == present_word:
        vocabulary[word[0]] += [[word[1],word[2]]]
    else:
        present_word = word[0]
        vocabulary[word[0]] = [[word[1],word[2]]]


# sorting the postings of a particular word
    for key in vocabulary:
        vocabulary[key].sort(key=itemgetter(0))


# information of doc_freq included in vocabulary
#for key in vocabulary:
#    update = (key,len(vocabulary[key]))






