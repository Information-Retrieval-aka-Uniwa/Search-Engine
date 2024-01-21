""""""""""""""""""""""""""""""""""""""""""""" 
    
    Βήμα 4. Κατάταξη αποτελεσμάτων (Ranking)
    
"""""""""""""""""""""""""""""""""""""""""""""
import math
from collections import Counter

# ------ Βήμα 4.ε. Κατάταξη αποτελεσμάτων (Ranking) ------
def calculate_tf(term_freq):
    max_freq = max(term_freq.values())
    tf = {term: freq / max_freq for term, freq in term_freq.items()}
    return tf

def calculate_idf(docs, term):
    num_documents_with_word = sum(1 for doc in docs if term in doc)
    idf = math.log(len(docs) / (1 + num_documents_with_word))
    return idf

def calculate_tfidf(query, docs):
    term_freq = Counter(query)
    tf = calculate_tf(term_freq)
    tfidf = {term: tf[term] * calculate_idf(docs, term) for term in term_freq}
    return tfidf

def cosine_similarity(tfidf_query, tfidf_docs):
    tfidf_query = [val for val in tfidf_query.values()] 
    tfidf_docs = [val for val in tfidf_docs.values()]

    dot_prod = 0.0
    for i, v in enumerate(tfidf_docs):
        dot_prod += v * tfidf_query[i]

    mag_1 = math.sqrt(sum([x**2 for x in tfidf_query]))
    mag_2 = math.sqrt(sum([x**2 for x in tfidf_docs]))

    return dot_prod / (mag_1 * mag_2) 

def rank_documents_vsm(docs, cosine_similarities):
    results = [(docs[i], cosine_similarities[i]) for i in range(len(docs))]
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def rank_documents_bm25(okapi_bm25_scores):
    okapi_bm25_scores.sort(key=lambda x: x['score'], reverse=True)
    results = [(doc['doc_id'], doc['score']) for doc in okapi_bm25_scores] 
    return results

