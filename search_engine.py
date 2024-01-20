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
    def __init__(self):
        self.data = {}                   # papers in dictionary format
        self.preprocessed_data = {}      # papers with preprocessed data in dictionary format
        self.inverted_index = {}         # inverted index
        self.boolean_retrieval_results = []             # List of papers that match the search query using the Boolean Retrieval algorithm
        self.vector_space_model_results = []            # List of papers that match the search query using the Vector Space Model algorithm
        self.okapi_bm_25_results = []                   # List of papers that match the search query using the Okapi BM25 algorithm

    """
    def __init__(self, json_data, json_preprocessed_data, inverted_index):   # Constructor της κλάσης SearchEngine
        with open(json_data, 'r') as file:
            self.data = json.load(file)                 # papers σε μορφή λεξικού 
        with open(json_preprocessed_data, 'r') as file:
            self.preprocessed_data = json.load(file)    # papers σε μορφή λεξικού με προεπεξεργασμένα δεδομένα
        self.inverted_index = inverted_index            # Ανεστραμμένο ευρετήριο
    """


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
            #documents = web_scrape(search_query)
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
            self.search_papers_boolean_retrieval(search_query)
            print(self.boolean_retrieval_results)
        elif retrieval_algorithm == "Vector Space Model":
            self.search_papers_vector_space_model(search_query)
            # Print the ranked documents
            for paper, similarity in self.vector_space_model_results:    # Εκτύπωση των αριθμών των εργασιών και των συνημιτονικών ομοιοτήτων τους
                print(f"Similarity: {similarity:.4f}\n{paper}\n")
        elif retrieval_algorithm == "Okapi BM25":
            self.search_papers_okapi_bm25(search_query)
            for paper, score in self.okapi_bm_25_results:    # Εκτύπωση των αριθμών των εργασιών και των συνημιτονικών ομοιοτήτων τους
                print(f"Score: {score:.4f}\n{paper}\n")
           

    
    def search_papers_boolean_retrieval(self, query):
        terms = query.lower().split()  # Μετατροπή του ερωτήματος αναζήτησης σε πεζά γράμματα και διαχωρισμός του σε λεκτικές μονάδες        
        for i, term in enumerate(terms):
            if term == "and" and i > 0 and i < len(terms) - 1:             # Έλεγχος για το αν ο όρος κλειδί (term) είναι "and" και αν βρίσκεται μεταξύ δύο όρων κλειδιών (terms)
                previous_term = terms[i - 1]                               # Αρχικοποίηση του προηγούμενου όρου κλειδιού (previous_term) από τον όρο κλειδί (term) που εξετάζουμε
                next_term = terms[i + 1]                                   # Αρχικοποίηση του επόμενου όρου κλειδιού (next_term) από τον όρο κλειδί (term) που εξετάζουμε
                papers_with_previous_term = []                          # Αρχικοποίηση της λίστας με τους αριθμούς των εργασιών που περιέχουν τον προηγούμενο όρο κλειδί (previous_term)
                papers_with_next_term = []                              # Αρχικοποίηση της λίστας με τους αριθμούς των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                if previous_term in self.inverted_index:
                    papers_with_previous_term = self.inverted_index[previous_term] # Ανάκτηση των αριθμών των εργασιών που περιέχουν τον προηγούμενο όρο κλειδί (previous_term)
                    for paper in papers_with_previous_term:                # Προσπέλαση των αριθμών των εργασιών που περιέχουν τον προηγούμενο όρο κλειδί (previous_term)
                        self.boolean_retrieval_results.append(paper)                         # Προσθήκη του αριθμού της εργασίας στη λίστα με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης
                if next_term in self.inverted_index:
                    papers_with_next_term = self.inverted_index[next_term]         # Ανάκτηση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                    for paper in papers_with_next_term:                    # Προσπέλαση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                        self.boolean_retrieval_results.append(paper)                         # Προσθήκη του αριθμού της εργασίας στη λίστα με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης
            
                if (len(papers_with_previous_term) > 0 and len(papers_with_next_term) > 0): # και οι δύο όροι κλειδιά (terms) υπάρχουν στο ευρετήριο
                    self.boolean_retrieval_results = set(papers_with_previous_term) & set(papers_with_next_term)
            
            elif term == "or" and i > 0 and i < len(terms) - 1:                  # Έλεγχος για το αν ο όρος κλειδί (term) είναι "or" και αν βρίσκεται μεταξύ δύο όρων κλειδιών (terms)
                previous_term = terms[i - 1]                                     # Αρχικοποίηση του προηγούμενου όρου κλειδιού (previous_term) από τον όρο κλειδί (term) που εξετάζουμε
                next_term = terms[i + 1]                                         # Αρχικοποίηση του επόμενου όρου κλειδιού (next_term) από τον όρο κλειδί (term) που εξετάζουμε
                if previous_term in self.inverted_index:
                    papers_with_previous_term = self.inverted_index[previous_term] # Ανάκτηση των αριθμών των εργασιών που περιέχουν τον προηγούμενο όρο κλειδί (previous_term)
                    for paper in papers_with_previous_term:                # Προσπέλαση των αριθμών των εργασιών που περιέχουν τον προηγούμενο όρο κλειδί (previous_term)
                        self.boolean_retrieval_results.append(paper)                         # Προσθήκη του αριθμού της εργασίας στη λίστα με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης
                if next_term in self.inverted_index:
                    papers_with_next_term = self.inverted_index[next_term]         # Ανάκτηση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                    for paper in papers_with_next_term:                    # Προσπέλαση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                        self.boolean_retrieval_results.append(paper)                         # Προσθήκη του αριθμού της εργασίας στη λίστα με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης

            elif term == "not" and i < len(terms) - 1:                           # Έλεγχος για το αν ο όρος κλειδί (term) είναι "not" και αν βρίσκεται πριν τον τελευταίο όρο κλειδί (terms)
                next_term = terms[i + 1]                                         # Αρχικοποίηση του επόμενου όρου κλειδιού (next_term) από τον όρο κλειδί (term) που εξετάζουμε
                if next_term in self.inverted_index:
                    papers_with_next_term = self.inverted_index[next_term]         # Ανάκτηση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                    all_papers = set(range(len(self.data)))                       # Αρχικοποίηση της λίστας με όλους τους αριθμούς των εργασιών και μετατροπή της σε σύνολο
                    self.boolean_retrieval_results = all_papers - set(papers_with_next_term) # Αφαίρεση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term) από τη λίστα με όλους τους αριθμούς των εργασιών και μετατροπή της σε σύνολο

    def search_papers_vector_space_model(self, query):
        # Step 1: Tokenize and preprocess the text
        tokenized_query = nltk.word_tokenize(preprocess_text(query))                         # Μετατροπή του ερωτήματος αναζήτησης σε λεκτικές μονάδες και προεπεξεργασία του κειμένου
        paper_id = [paper['id'] for paper in self.data]                                               # Λίστα με τους αριθμούς των εργασιών
        #title = [doc['title'] for doc in papers]
        preprocessed_abstracts = [paper['abstract'] for paper in self.preprocessed_data]            # Λίστα με τις προεπεξεργασμένες περιλήψεις (abstracts) των εργασιών
        tokenized_abstracts = [nltk.word_tokenize(paper) for paper in preprocessed_abstracts]    # Λίστα με τις λεκτικές μονάδες των προεπεξεργασμένων περιλήψεων (abstracts) των εργασιών

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
        self.vector_space_model_results = [(paper_id[i], cosine_similarities[0][i]) for i in range(len(paper_id))]       # Αποθήκευση των αριθμών των εργασιών και των συνημιτονικών ομοιοτήτων τους σε μία λίστα
        self.vector_space_model_results.sort(key=lambda x: x[1], reverse=True)                                       # Ταξινόμηση του αποτελέσματος


    def search_papers_okapi_bm25(self, query):
        for paper in self.preprocessed_data:
            paper['score'] = self.calculate_okapi_bm25_score(query, paper['abstract'])
            self.okapi_bm_25_results.append(paper)
        self.okapi_bm_25_results.sort(key=lambda x: x['score'], reverse=True)  # Sort the results by 'score'
        self.okapi_bm_25_results = [(paper['id'], paper['score']) for paper in self.okapi_bm_25_results]  # Store the sorted results in a list of tuples
    
    def calculate_okapi_bm25_score(self, query, paper, k = 1.2, b = 0.75):
        score = 0
        # Calculate document length
        paper_length = len(paper)
    
        # Calculate average document length
        total_papers = len(self.inverted_index.keys())
        total_paper_length = sum([len(paper) for paper in self.inverted_index.values()])
        average_paper_length = total_paper_length / total_papers
    
        # Calculate IDF for each term in the query
        for term in query:
            if term in self.inverted_index:
                paper_frequency = len(self.inverted_index[term])
                inverse_paper_frequency = math.log((total_papers - paper_frequency + 0.5) / (paper_frequency + 0.5))
            
                # Calculate term frequency in the document
                term_frequency = paper.count(term)
            
                # Calculate BM25 score for the term
                score += inverse_paper_frequency * ((term_frequency * (k + 1)) / (term_frequency + k * (1 - b + b * (paper_length / average_paper_length))))
    
        return score
    
                 
        



