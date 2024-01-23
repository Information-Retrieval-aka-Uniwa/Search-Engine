""""""""""""""""""""""""""""""""""""""""""""" 
    
    Βήμα 4. Κατάταξη αποτελεσμάτων (Ranking)
    
"""""""""""""""""""""""""""""""""""""""""""""
import math
import nltk
from collections import Counter

# ------ Βήμα 4.ε. Κατάταξη αποτελεσμάτων (Ranking) ------
# ------ TF-IDF για τους όρους των εργασιών ------
def calculate_tfidf_docs(docs):
    
    # ------ Tokenize και προεπεξεργασία των όρων των εργασιών ------
    abstracts = [doc['abstract'] for doc in docs] 
    tokenized_docs = [nltk.word_tokenize(doc.lower()) for doc in abstracts] 
    # ------ Υπολογισμός TF ------
    tf = [Counter(doc) for doc in tokenized_docs]                                       # Η συχνότητα εμφάνισης κάθε όρου στο κείμενο
    # ------ Υπολογισμός DF ------
    df = Counter(term for doc in tokenized_docs for term in doc)                        # Ο αριθμός των εγγράφων που εμφανίζεται ο κάθε όρος
    # ------ Υπολογισμός IDF ------
    idf = {term: math.log(len(docs) / freq) for term, freq in df.items()}               # Ο αριθμός των εγγράφων που εμφανίζεται ο κάθε όρος
    # ------ Υπολογισμός TF-IDF ------
    tfidf_docs = [{term: freq * idf[term] for term, freq in doc.items()} for doc in tf] # Η συχνότητα εμφάνισης κάθε όρου στο κείμενο

    return tfidf_docs, idf

# ------ TF-IDF για τους όρους του ερωτήματος χρήστη ------
def calculate_tfidf_query(query, idf_docs):
   
    # ------ Tokenize και προεπεξεργασία των όρων του ερωτήματος χρήστη ------
    tokenized_query = nltk.word_tokenize(query.lower()) 
    # ------ Υπολογισμός TF-IDF ------
    tfidf_query = {term: tokenized_query.count(term) * idf_docs.get(term, 0) for term in tokenized_query} # Η συχνότητα εμφάνισης κάθε όρου του ερωτήματος χρήστη σε κάθε κείμενο

    return tfidf_query

# ------ Υπολογισμός ομοιότητας μεταξύ του ερωτήματος χρήστη και των εγγράφων ------
def calculate_cosine_similarity(tfidf_query, doc):
    
    dot_product = sum(tfidf_query.get(term, 0) * doc.get(term, 0) for term in tfidf_query) # Το εσωτερικό γινόμενο των διανυσμάτων του ερωτήματος χρήστη και του κειμένου
    norm_query = math.sqrt(sum(val**2 for val in tfidf_query.values()))                    # Η Ευκλείδεια απόσταση του διανύσματος του ερωτήματος χρήστη
    norm_doc = math.sqrt(sum(val**2 for val in doc.values()))                              # Η Ευκλείδεια απόσταση του διανύσματος του κειμένου
    cosine_similarity = dot_product / (norm_query * norm_doc)                              # Η ομοιότητα μεταξύ του ερωτήματος χρήστη και του κειμένου

    return cosine_similarity

# ------ Κατάταξη των εγγράφων με βάση την ομοιότητα συνημιτόνου ------
def rank_documents_vsm(docs, cosine_similarities):
    
    results = [(docs[i], cosine_similarities[i]) for i in range(len(docs))]
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results

def rank_documents_bm25(okapi_bm25_scores):
    
    okapi_bm25_scores.sort(key=lambda x: x['score'], reverse=True)
    results = [(doc['doc_id'], doc['score']) for doc in okapi_bm25_scores] 
    
    return results

