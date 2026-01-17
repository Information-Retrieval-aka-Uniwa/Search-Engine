""""""""""""""""""""""""""""""""""""""""""""" 
    
    Step 4. Ranking
    
"""""""""""""""""""""""""""""""""""""""""""""
import math
from collections import Counter

from text_preprocessing import preprocess_text

# ------ Ranking of results ------
# ------ TF-IDF for the terms of the documents ------
def calculate_tfidf_docs(docs):
    
    # ------ Tokenize and preprocess the terms of the documents ------
    abstracts = [doc['abstract'] for doc in docs] 
    tokenized_docs = [preprocess_text('abstract', doc).split() for doc in abstracts] 
    # ------ Calculation Term Frequency ------
    tf = [Counter(doc) for doc in tokenized_docs]                                       # The frequency of each term in the document
    # ------ Calculation Document Frequency ------
    df = Counter(term for doc in tokenized_docs for term in doc)                        # The number of documents that contain each term
    # ------ Calculation Inverse Document Frequency ------
    idf = {term: math.log(len(docs) / freq) for term, freq in df.items()}               # The number of documents that contain each term
    # ------ Calculation TF-IDF ------
    tfidf_docs = [{term: freq * idf[term] for term, freq in doc.items()} for doc in tf] # The frequency of each term in the document

    return tfidf_docs, idf

# ------ TF-IDF for the terms of the user query ------
def calculate_tfidf_query(query, idf_docs):
   
    # ------ Tokenize and preprocess the terms of the user query ------
    tokenized_query = preprocess_text('query', query).split()
    # ------ Calculation TF-IDF ------
    tfidf_query = {term: tokenized_query.count(term) * idf_docs.get(term, 0) for term in tokenized_query} # The frequency of each term in the user query

    return tfidf_query

# ------ Calculation of similarity between the user query and the documents ------
def calculate_cosine_similarity(tfidf_query, doc):
    
    dot_product = sum(tfidf_query.get(term, 0) * doc.get(term, 0) for term in tfidf_query) # The dot product of the vectors of the user query and the document
    norm_query = math.sqrt(sum(val**2 for val in tfidf_query.values()))                    # The Euclidean distance of the vector of the user query
    norm_doc = math.sqrt(sum(val**2 for val in doc.values()))                              # The Euclidean distance of the vector of the document
    if norm_query != 0 and norm_doc != 0:
        cosine_similarity = dot_product / (norm_query * norm_doc)                          # The similarity between the user query and the document
    else:
        cosine_similarity = 0

    return cosine_similarity

# ------ Ranking of documents based on cosine similarity ------
def rank_documents_vsm(docs, cosine_similarities):
    
    results = [(docs[i], cosine_similarities[i]) for i in range(len(docs))]
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results

def calculate_okapi_bm25_score(query, inverted_index, doc, k = 1.2, b = 0.75):
    preprocessed_query = preprocess_text('query', query)
    score = 0
    # ------ Calculation of document length ------
    doc_length = len(doc)
    # ------ Calculation of average document length in the collection ------
    total_docs = len(inverted_index.keys())
    total_doc_length = sum([len(doc) for doc in inverted_index.values()])
    average_doc_length = total_doc_length / total_docs
    # ------ Calculation TF-IDF for each term in the query ------
    for term in preprocessed_query:
        if term in inverted_index:
            # ------ Calculation Document Frequency ------ 
            doc_frequency = len(inverted_index[term])
            # ------ Calculation Inverted Document Frequency ------
            inverse_doc_frequency = math.log((total_docs - doc_frequency + 0.5) / (doc_frequency + 0.5))
            # ------ Calculation TF ------
            term_frequency = doc.count(term)
            # ------ Calculation BM25 coefficient for each term in the query ------
            score += inverse_doc_frequency * ((term_frequency * (k + 1)) / (term_frequency + k * (1 - b + b * (doc_length / average_doc_length))))
    
    return score

def rank_documents_bm25(okapi_bm25_scores):
    
    okapi_bm25_scores.sort(key=lambda x: x['score'], reverse=True)
    results = [(doc['doc_id'], doc['score']) for doc in okapi_bm25_scores] 
    
    return results

