import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

def get_tokens(text):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    return tokens

def remove_stop_words(tokens):
    sr = stopwords.words('english')
    for token in tokens:
        if token in sr:
            tokens.remove(token)
    return tokens

def normalization(tokens):
    lemmatizer = WordNetLemmatizer()
    for index, token in enumerate(tokens):
        tokens[index] = str(lemmatizer.lemmatize(token.lower()))
    return tokens

def get_term_frequencies(text, doc_id):
    tokens = get_tokens(text)
    stop_tokens = remove_stop_words(tokens)
    lemma_tokens = normalization(stop_tokens)
    lemma_tokens.sort()
    freq = nltk.FreqDist(lemma_tokens)
    term_freqs = []
    for key, val in freq.items():
        term_freqs = term_freqs + [[str(key), doc_id, val]]
    return term_freqs
