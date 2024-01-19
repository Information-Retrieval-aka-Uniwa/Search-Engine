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



"""
def create_inverted_index(data):
    
    inverted_index = {}                             # Αρχικοποίηση της ανεστραμμένης δομής δεδομένων ευρετηρίου (δομή λεξικού)
    for paper_id, abstract in enumerate(data):   # Προσπέλαση της λίστας με τις περιλήψεις (abstract) των εργασιών (doc_id --> Θέση της περίληψης στην λίστα, document --> Περίληψη)
        for word in abstract.split():               # Χωρισμός της περίληψης document σε λεκτικές μονάδες και προσπέλαση αυτών. Η προεπεξεργασία κειμένου έχει γίνει οπότε αρκεί η str.split() αντί της nltk.word_tokenize() για τον χωρισμό
            if word not in inverted_index:          # O όρος κλειδί (word) δεν υπάρχει στο ευρετήριο 
                inverted_index[word] = set()        # Το ευρετήριο είναι ένα λεξικό οπότε ορίζουμε το κλειδί word με κενό περιεχόμενο
            inverted_index[word].add(doc_id)        # Προσθήκη του αριθμού της περίληψης (abs_id) στο περιεχόμενο με κλειδί τον όρο word. Η λέξη word εμφανίζεται στη περίληψη της εργασίας με abs_id

    return inverted_index                           # Επιστροφή της ανεστραμμένης δομής δεδομένων ευρετηρίου (δομή λεξικού)                 
"""
       


