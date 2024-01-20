"""
Βήμα 3. Ευρετήριο (Indexing)

Είσοδος[1]    --> [abstracts]       Μία λίστα με τις περιλήψεις (abstracts) των εργασιών που συλλέξαμε στο 'Βήμα 1. Σταχυολογητής (Web Crawler)' και κάναμε προεπεξεργασία κειμένου στο 'Βήμα 2. Προεπεξεργασία κειμένου'
Λειτουργία    -->                   Αντιστοιχίζει κάθε λέξη/όρο με τον αριθμό ή αριθμούς (abs_id) των περιλήψεων (abstract) των εργασιών, στην οποία εμφανίζεται
Έξοδος[1]     --> [inverted_index]  Ανεστραμμένη δομή δεδομένων ευρετηρίου (inverted_index)
    
"""
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
    
    return inverted_index                     # Επιστροφή του ανεστραμμένου ευρετηρίου (inverted_index)




       


