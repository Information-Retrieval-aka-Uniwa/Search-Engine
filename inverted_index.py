

def create_inverted_index(documents):      # Αντιστοιχίζει κάθε λέξη με τον αριθμό του εγγράφου στο οποίο εμφανίζεται
    inverted_index = {}                    # Αρχικοποίηση του αντιστρόφου ευρετηρίου
    for doc_id, document in enumerate(documents):
        for word in document.split():
            if word not in inverted_index:   # Αν το κλειδί/λέξη δεν υπάρχει στο ευρετήριο τότε βάζει την λέξη στο ευρετήριο
                inverted_index[word] = set() # Αρχικοποίηση του συνόλου με τη λέξη κλειδί word
            inverted_index[word].add(doc_id) # Προσθήκη του αριθμού του εγγράφου στο ευρετήριο με λέξη κλειδί word
    return inverted_index


