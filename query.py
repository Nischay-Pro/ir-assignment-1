import nltk
import individual_file
import experiment

query = input("Search for News :) ")
tokens = individual_file.get_tokens(query)
stop_tokens = individual_file.remove_stop_words(tokens)
lemma_tokens = individual_file.normalization(stop_tokens)
lemma_tokens.sort()
freq = nltk.FreqDist(lemma_tokens)
term_freqs = []
for key, val in freq.items():
    term_freqs = term_freqs + [[str(key), val]]

