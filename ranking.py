import math
from collections import Counter

def calculate_tf(term_freq):
    max_freq = max(term_freq.values())
    tf = {term: freq / max_freq for term, freq in term_freq.items()}
    return tf

def calculate_idf(corpus, term):
    num_documents_with_word = sum(1 for doc in corpus if term in doc)
    idf = math.log(len(corpus) / (1 + num_documents_with_word))
    return idf

def calculate_tfidf(doc, corpus):
    term_freq = Counter(doc)
    tf = calculate_tf(term_freq)
    tfidf = {term: tf[term] * calculate_idf(corpus, term) for term in term_freq}
    return tfidf

# Example usage
corpus = [
    ['apple', 'banana', 'apple'],
    ['banana', 'orange'],
    ['apple', 'orange', 'orange']
]

document = ['apple', 'banana']

tfidf = calculate_tfidf(document, corpus)
print(tfidf)
