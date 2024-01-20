import json
import tkinter
import nltk 
from tkinter import ttk

#from retrieval_algos import search_papers_boolean, search_papers_default, search_papers_vector_space
import tkinter
from tkinter import ttk

from text_preprocessing import preprocess_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math

from web_crawler import web_crawling, store_json

"""
Βήμα 4. Μηχανή αναζήτησης (Search engine)

def init_gui(papers, inverted_dict)

Είσοδος[1] --> [papers]          Λίστα με τα δεδομένα κάθε εργασίας δομημένα σε μία δομή λεξικού με κλειδία τα ονόματα των δεδομένων και αντίστοιχα περιεχόμενα τα δεδομένα    
Είσοδος[2] --> [inverted_index]  Ανεστραμμένη δομή δεδομένων ευρετηρίου αποθηκευμένη σε μία δομή λεξικού 
Λειτουργία -->                   Αρχικοποίηση της διεπαφής χρήστη για την αναζήτηση εργασιών 
    
"""
"""
Βήμα 4. Μηχανή αναζήτησης (Search engine)

def print_papers(search_query, papers, inverted_dict)

Είσοδος[1] --> [search_query]    Ερώτημα αναζήτησης που εισήγαγε ο χρήστης στην διεπαφή χρήστη
Είσοδος[2] --> [papers]          Λίστα με τα δεδομένα κάθε εργασίας δομημένα σε μία δομή λεξικού με κλειδία τα ονόματα των δεδομένων και αντίστοιχα περιεχόμενα τα δεδομένα    
Είσοδος[3] --> [inverted_index]  Ανεστραμμένη δομή δεδομένων ευρετηρίου αποθηκευμένη σε μία δομή λεξικού 
Λειτουργία -->                   Εκτύπωση των ακαδημαϊκών εργασιών που περιέχουν το ερώτημα αναζήτησης 
    
"""

class SearchEngine:
    def __init__(self, inverted_index):
        with open('dataset.json', 'r') as file:
            self.dataset = json.load(file)                 # papers σε μορφή λεξικού
        with open('preprocessed_dataset.json', 'r') as file:
            self.preprocessed_dataset = json.load(file)
        self.inverted_index = inverted_index         # inverted index

    def init_gui(self):
        # ----- Παράθυρο διεπαφής χρήστη -----
        window = tkinter.Tk()                          # Αρχικοποίηση του παραθύρου της διεπαφής χρήστη
        window.title("Αναζήτηση ακαδημαϊκών εργασιών") # Ορισμός του τίτλου του παραθύρου
        window.geometry("400x200")                     # Ορισμός του μεγέθους του παραθύρου

        # ----- Πεδίο εισαγωγής κειμένου -----
        search_entry = tkinter.Entry(window, width=50) # Ορισμός του πλάτους του πεδίου εισαγωγής κειμένου
        search_entry.pack(pady=10)                     # Ορισμός του πεδίου εισαγωγής κειμένου στο παράθυρο

        # ----- Πεδίο επιλογής αλγορίθμου ανάκτησης -----
        options = ["Boolean Retrieval", "Vector Space Model", "Okapi BM25"]         # Ορισμός των επιλογών του πεδίου επιλογής αλγορίθμου ανάκτησης    
        combobox = ttk.Combobox(window, values=options, state="readonly", width=30) # Ορισμός του πλάτους του πεδίου επιλογής αλγορίθμου ανάκτησης, των επιλογών του πεδίου επιλογής αλγορίθμου ανάκτησης, της κατάστασης του πεδίου επιλογής αλγορίθμου ανάκτησης (readonly) και της δημιουργίας του πεδίου επιλογής αλγορίθμου ανάκτησης
        combobox.set("Επιλογή Αλγορίθμου Ανάκτησης")                                # Ορισμός της προεπιλεγμένης επιλογής του πεδίου επιλογής αλγορίθμου ανάκτησης
        combobox.pack()                                                             # Ορισμός του πεδίου επιλογής αλγορίθμου ανάκτησης στο παράθυρο

        # ----- Ερώτημα αναζήτησης (query) -----
        def get_query():                                        # Inline συνάρτηση που επιστρέφει το query που εισήγαγε ο χρήστης στην διεπαφή χρήστη
            search_query = search_entry.get()                   # Το query που εισήγαγε ο χρήστης στην διεπαφή χρήστη
            retrieval_algorithm = combobox.get()                 # Επιλεγμένος αλγόριθμος ανάκτησης
            print("Selected Algorithm:", retrieval_algorithm)    # Εκτύπωση του επιλεγμένου αλγορίθμου ανάκτησης
            self.search_papers(search_query, retrieval_algorithm)  # Κλήση της print_papers για την εκτύπωση των δεδομένων των εργασιών που περιέχουν το ερώτημα αναζήτησης

        # ----- Κουμπί αναζήτησης -----
        search_button = tkinter.Button(window, text="Αναζήτηση", command=get_query) # Ορισμός του κουμπιού αναζήτησης και κλήση της inline συνάρτησης get_query, όταν πατηθεί το κουμπί
        search_button.pack()                                                        # Ορισμός του κουμπιού αναζήτησης στο παράθυρο

        # ----- Εκτέλεση του παραθύρου -----
        window.mainloop()

    def search_papers(self, search_query, retrieval_algorithm):

        if retrieval_algorithm == "Boolean Retrieval":
            results_boolean = self.search_papers_boolean_retrieval(search_query)
            print(results_boolean)
        elif retrieval_algorithm == "Vector Space Model":
            results_vsm = self.search_papers_vector_space_model(search_query)
            # Print the ranked documents
            for paper, similarity in results_vsm:    # Εκτύπωση των αριθμών των εργασιών και των συνημιτονικών ομοιοτήτων τους
                print(f"Similarity: {similarity:.4f}\n{paper}\n")
        elif retrieval_algorithm == "Okapi BM25":
            results_bm25 = self.search_papers_okapi_bm25(search_query)
            for paper, score in results_bm25:    # Εκτύπωση των αριθμών των εργασιών και των συνημιτονικών ομοιοτήτων τους
                print(f"Score: {score:.4f}\n{paper}\n")
           

    
    def search_papers_boolean_retrieval(self, query):
        terms = query.lower().split()  # Μετατροπή του ερωτήματος αναζήτησης σε πεζά γράμματα και διαχωρισμός του σε λεκτικές μονάδες        
        boolean_retrieval_results = []  # Αρχικοποίηση της λίστας με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης
        for i, term in enumerate(terms):
            if term == "and" and i > 0 and i < len(terms) - 1:             # Έλεγχος για το αν ο όρος κλειδί (term) είναι "and" και αν βρίσκεται μεταξύ δύο όρων κλειδιών (terms)
                previous_term = terms[i - 1]                               # Αρχικοποίηση του προηγούμενου όρου κλειδιού (previous_term) από τον όρο κλειδί (term) που εξετάζουμε
                next_term = terms[i + 1]                                   # Αρχικοποίηση του επόμενου όρου κλειδιού (next_term) από τον όρο κλειδί (term) που εξετάζουμε
                docs_with_previous_term = []                          # Αρχικοποίηση της λίστας με τους αριθμούς των εργασιών που περιέχουν τον προηγούμενο όρο κλειδί (previous_term)
                docs_with_next_term = []                              # Αρχικοποίηση της λίστας με τους αριθμούς των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                if previous_term in self.inverted_index:
                    docs_with_previous_term = self.inverted_index[previous_term] # Ανάκτηση των αριθμών των εργασιών που περιέχουν τον προηγούμενο όρο κλειδί (previous_term)
                    for doc in docs_with_previous_term:                # Προσπέλαση των αριθμών των εργασιών που περιέχουν τον προηγούμενο όρο κλειδί (previous_term)
                        boolean_retrieval_results.append(doc)                         # Προσθήκη του αριθμού της εργασίας στη λίστα με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης
                if next_term in self.inverted_index:
                    docs_with_next_term = self.inverted_index[next_term]         # Ανάκτηση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                    for doc in docs_with_next_term:                    # Προσπέλαση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                        boolean_retrieval_results.append(doc)                         # Προσθήκη του αριθμού της εργασίας στη λίστα με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης
            
                if (len(docs_with_previous_term) > 0 and len(docs_with_next_term) > 0): # και οι δύο όροι κλειδιά (terms) υπάρχουν στο ευρετήριο
                    boolean_retrieval_results = sorted(set(docs_with_previous_term) & set(docs_with_next_term))
                elif len(docs_with_previous_term) > 0:
                    boolean_retrieval_results = set(docs_with_previous_term)
                elif len(docs_with_next_term) > 0:
                    boolean_retrieval_results = set(docs_with_next_term)
            
            elif term == "or" and i > 0 and i < len(terms) - 1:                  # Έλεγχος για το αν ο όρος κλειδί (term) είναι "or" και αν βρίσκεται μεταξύ δύο όρων κλειδιών (terms)
                previous_term = terms[i - 1]                                     # Αρχικοποίηση του προηγούμενου όρου κλειδιού (previous_term) από τον όρο κλειδί (term) που εξετάζουμε
                next_term = terms[i + 1]                                         # Αρχικοποίηση του επόμενου όρου κλειδιού (next_term) από τον όρο κλειδί (term) που εξετάζουμε
                if previous_term in self.inverted_index:
                    docs_with_previous_term = self.inverted_index[previous_term] # Ανάκτηση των αριθμών των εργασιών που περιέχουν τον προηγούμενο όρο κλειδί (previous_term)
                    for doc in docs_with_previous_term:                # Προσπέλαση των αριθμών των εργασιών που περιέχουν τον προηγούμενο όρο κλειδί (previous_term)
                        boolean_retrieval_results.append(doc)                         # Προσθήκη του αριθμού της εργασίας στη λίστα με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης
                if next_term in self.inverted_index:
                    docs_with_next_term = self.inverted_index[next_term]         # Ανάκτηση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                    for doc in docs_with_next_term:                    # Προσπέλαση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                        boolean_retrieval_results.append(doc) 
                
                if (len(docs_with_previous_term) > 0 and len(docs_with_next_term) > 0): # και οι δύο όροι κλειδιά (terms) υπάρχουν στο ευρετήριο
                    boolean_retrieval_results = sorted(set(docs_with_previous_term) | set(docs_with_next_term))                      # Προσθήκη του αριθμού της εργασίας στη λίστα με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης
                elif len(docs_with_previous_term) > 0:
                    boolean_retrieval_results = set(docs_with_previous_term)
                elif len(docs_with_next_term) > 0:
                    boolean_retrieval_results = set(docs_with_next_term)
                    
            elif term == "not" and i < len(terms) - 1:                           # Έλεγχος για το αν ο όρος κλειδί (term) είναι "not" και αν βρίσκεται πριν τον τελευταίο όρο κλειδί (terms)
                next_term = terms[i + 1]                                         # Αρχικοποίηση του επόμενου όρου κλειδιού (next_term) από τον όρο κλειδί (term) που εξετάζουμε
                if next_term in self.inverted_index:
                    docs_with_next_term = self.inverted_index[next_term]         # Ανάκτηση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                    all_docs = set(range(len(self.dataset)))                       # Αρχικοποίηση της λίστας με όλους τους αριθμούς των εργασιών και μετατροπή της σε σύνολο
                    boolean_retrieval_results = sorted(all_docs - set(docs_with_next_term)) # Αφαίρεση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term) από τη λίστα με όλους τους αριθμούς των εργασιών και μετατροπή της σε σύνολο
        
        return boolean_retrieval_results


    def search_papers_vector_space_model(self, query):
        vector_space_model_results = []
        # Step 1: Tokenize and preprocess the text
        tokenized_query = nltk.word_tokenize(preprocess_text('query', query))                         # Μετατροπή του ερωτήματος αναζήτησης σε λεκτικές μονάδες και προεπεξεργασία του κειμένου
        doc_id = [doc['doc_id'] for doc in self.dataset]                                               # Λίστα με τους αριθμούς των εργασιών
        #title = [doc['title'] for doc in papers]
        preprocessed_abstracts = [doc['abstract'] for doc in self.preprocessed_dataset]            # Λίστα με τις προεπεξεργασμένες περιλήψεις (abstracts) των εργασιών
        tokenized_abstracts = [nltk.word_tokenize(doc) for doc in preprocessed_abstracts]    # Λίστα με τις λεκτικές μονάδες των προεπεξεργασμένων περιλήψεων (abstracts) των εργασιών

        # Step 2: Calculate TF-IDF
        # Convert tokenized documents to text
        preprocessed_abstracts = [' '.join(paper) for paper in tokenized_abstracts]              # Μετατροπή των λεκτικών μονάδων των περιλήψεων (abstracts) σε κείμενο
        preprocessed_query = ' '.join(tokenized_query)                                       # Μετατροπή των λεκτικών μονάδων του ερωτήματος αναζήτησης σε κείμενο

        # Create a TF-IDF vectorizer
        tfidf_vectorizer = TfidfVectorizer()                                                 # Δημιουργία ενός TF-IDF vectorizer
        tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_abstracts)                # Μετατροπή των προεπεξεργασμένων περιλήψεων (abstracts) σε TF-IDF vectors

        # Transform the query into a TF-IDF vector
        query_vector = tfidf_vectorizer.transform([preprocessed_query])                      # Μετατροπή του ερωτήματος αναζήτησης σε TF-IDF vector

        # Step 3: Calculate cosine similarity
        cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)                  # Υπολογισμός της συνημιτονικής ομοιότητας του ερωτήματος αναζήτησης με τα TF-IDF vectors των περιλήψεων (abstracts) των εργασιών

        # Step 4: Rank documents by similarity
        vector_space_model_results = [(doc_id[i], cosine_similarities[0][i]) for i in range(len(doc_id))]       # Αποθήκευση των αριθμών των εργασιών και των συνημιτονικών ομοιοτήτων τους σε μία λίστα
        vector_space_model_results.sort(key=lambda x: x[1], reverse=True)                                       # Ταξινόμηση του αποτελέσματος

        return vector_space_model_results

    def search_papers_okapi_bm25(self, query):
        okapi_bm_25_results = []
        for doc in self.preprocessed_dataset:
           doc['score'] = self.calculate_okapi_bm25_score(query, doc['abstract'])
           okapi_bm_25_results.append(doc)
        okapi_bm_25_results.sort(key=lambda x: x['score'], reverse=True)  # Sort the results by 'score'
        okapi_bm_25_results = [(doc['doc_id'], doc['score']) for doc in okapi_bm_25_results]  # Store the sorted results in a list of tuples
        
        return okapi_bm_25_results 
    
    def calculate_okapi_bm25_score(self, query, doc, k = 1.2, b = 0.75):
        score = 0
        # Calculate document length
        doc_length = len(doc)
    
        # Calculate average document length
        total_docs = len(self.inverted_index.keys())
        total_doc_length = sum([len(doc) for doc in self.inverted_index.values()])
        average_doc_length = total_doc_length / total_docs
    
        # Calculate IDF for each term in the query
        for term in query:
            if term in self.inverted_index:
                doc_frequency = len(self.inverted_index[term])
                inverse_doc_frequency = math.log((total_docs - doc_frequency + 0.5) / (doc_frequency + 0.5))
            
                # Calculate term frequency in the document
                term_frequency = doc.count(term)
            
                # Calculate BM25 score for the term
                score += inverse_doc_frequency * ((term_frequency * (k + 1)) / (term_frequency + k * (1 - b + b * (doc_length / average_doc_length))))
    
        return score
    
                 
        



