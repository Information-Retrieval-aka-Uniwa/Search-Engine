"""
Βήμα 3. Ευρετήριο (Indexing)

Είσοδος[1]    --> [abstracts]       Μία λίστα με τις περιλήψεις (abstracts) των εργασιών που συλλέξαμε στο 'Βήμα 1. Σταχυολογητής (Web Crawler)' και κάναμε προεπεξεργασία κειμένου στο 'Βήμα 2. Προεπεξεργασία κειμένου'
Λειτουργία    -->                   Αντιστοιχίζει κάθε λέξη/όρο με τον αριθμό ή αριθμούς (abs_id) των περιλήψεων (abstract) των εργασιών, στην οποία εμφανίζεται
Έξοδος[1]     --> [inverted_index]  Ανεστραμμένη δομή δεδομένων ευρετηρίου (inverted_index)
    
"""
def create_inverted_index(data):
    
    inverted_index = {}
    for paper in data:
        abstract = paper.get('abstract')
        terms = abstract.split()  # Split the abstract into individual terms
        for term in terms:
            if term not in inverted_index:
                inverted_index[term] = set()
            inverted_index[term].add(paper['id'])
    
    return inverted_index




       


