def create_inverted_index(preprocessed_dataset):
    
    inverted_index = {}                              # Αρχικοποίηση του ανεστραμμένου ευρετηρίου (inverted_index) σε κενό λεξικό
    for doc in preprocessed_dataset:                               # Προσπέλαση των δεδομένων των εργασιών
        abstract = doc.get('abstract')             # Ανάκτηση της περίληψης (abstract) της εργασίας
        terms = abstract.split()                     # Διαχωρισμός του κειμένου σε λεκτικές μονάδες
        for term in terms:                           # Προσπέλαση των λεκτικών μονάδων
            if term not in inverted_index:           # Έλεγχος για το αν ο όρος κλειδί (term) υπάρχει στο ανεστραμμένο ευρετήριο (inverted_index)
                inverted_index[term] = set()         # Αρχικοποίηση του συνόλου με τους αριθμούς των εργασιών που περιέχουν τον όρο κλειδί (term)
            inverted_index[term].add(doc['doc_id'])    # Προσθήκη του αριθμού της εργασίας στο σύνολο με τους αριθμούς των εργασιών που περιέχουν τον όρο κλειδί (term)
    
    inverted_index = dict(sorted(inverted_index.items()))  # Ταξινόμηση του ανεστραμμένου ευρετηρίου (inverted_index) βάσει των κλειδιών
    for term in inverted_index:                      # Ταξινόμηση των αριθμών των εργασιών για κάθε όρο κλειδί
        inverted_index[term] = sorted(inverted_index[term])


    return inverted_index                     # Επιστροφή του ανεστραμμένου ευρετηρίου (inverted_index)




       


