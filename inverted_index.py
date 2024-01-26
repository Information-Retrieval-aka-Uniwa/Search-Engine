""""""""""""""""""""""""""""""""""""""""""""" 
    
    Βήμα 3. Ευρετήριο (Indexing)
    
"""""""""""""""""""""""""""""""""""""""""""""

# ------ Βήμα 3.α. Δημιουργία της ανεστραμμένης δομής δεδομένων ευρετηρίου ------
def create_inverted_index(preprocessed_dataset):
    inverted_index = {}
    for doc in preprocessed_dataset:
        abstract = doc.get('abstract')
        terms = abstract.split()
        for term in terms:
            if term not in inverted_index:
                inverted_index[term] = set()
            inverted_index[term].add(doc['doc_id'])

    inverted_index = dict(sorted(inverted_index.items()))
    for term in inverted_index:
        inverted_index[term] = sorted(inverted_index[term])

    return inverted_index





       


