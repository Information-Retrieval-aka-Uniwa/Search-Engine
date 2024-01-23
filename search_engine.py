""""""""""""""""""""""""""""""""""""""""""""" 
    
    Βήμα 4. Μηχανή αναζήτησης (Search engine)
    
"""""""""""""""""""""""""""""""""""""""""""""
from collections import Counter
import json
import tkinter
import nltk
import math
from tkinter import ttk

import tkinter
from tkinter import ttk
from query_processing import query_processing, replace_terms_with_docs
from ranking import calculate_cosine_similarity, calculate_tfidf_docs, calculate_tfidf_query, rank_documents_vsm, rank_documents_bm25
from text_preprocessing import preprocess_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SearchEngine:

    def __init__(self, inverted_index):
        with open('dataset/dataset.json', 'r') as file:
            self.dataset = json.load(file)               
        with open('dataset/preprocessed_dataset.json', 'r') as file:
            self.preprocessed_dataset = json.load(file)
        self.inverted_index = inverted_index      

    # ------ Βήμα 4.α Ανάπτυξη διεπαφής χρήστη για αναζήτηση εργασιών ------
    def init_gui(self):
        # ----- Παράθυρο διεπαφής χρήστη -----
        window = tkinter.Tk()                      
        window.title("Αναζήτηση ακαδημαϊκών εργασιών")
        window.geometry("400x200")                   

        # ----- Πεδίο εισαγωγής κειμένου -----
        search_entry = tkinter.Entry(window, width=50) 
        search_entry.pack(pady=10)                 

        # ----- Πεδίο επιλογής αλγορίθμου ανάκτησης -----
        options = ["Boolean Retrieval", "Vector Space Model", "Okapi BM25"]           
        combobox = ttk.Combobox(window, values=options, state="readonly", width=30) 
        combobox.set("Επιλογή Αλγορίθμου Ανάκτησης")                                
        combobox.pack()                                                            

        # ----- Ερώτημα αναζήτησης (query) -----
        def get_query():                                     
            search_query = search_entry.get()                   
            retrieval_algorithm = combobox.get()          
            print(f"----------- Αλγόριθμος ανάκτησης: {retrieval_algorithm} -----------")  
            self.search_papers(search_query, retrieval_algorithm)  

        # ----- Κουμπί αναζήτησης -----
        search_button = tkinter.Button(window, text="Αναζήτηση", command=get_query)
        search_button.pack()                                                       

        # ----- Εκτέλεση του παραθύρου -----
        window.mainloop()

    # ------ Βήμα 4.β. Υλοποίηση αλγορίθμων ανάκτησης ------
    def search_papers(self, search_query, retrieval_algorithm):
        print(f'============ Ερώτημα αναζήτησης: {search_query} ============\n')
        if retrieval_algorithm == "Boolean Retrieval":
            results_boolean = self.search_papers_boolean_retrieval(search_query)
            for doc_id in results_boolean:
                for key, value in self.dataset[doc_id].items():
                    print(f"'{key}': '{value}'")
                print("\n")
            print("\n")
        elif retrieval_algorithm == "Vector Space Model":
            results_vsm = self.search_papers_vector_space_model(search_query)
            for paper, similarity in results_vsm:
                print(f"Similarity: {similarity:.4f}")
                for key, value in self.dataset[paper].items():
                    print(f"'{key}': '{value}'")
                print("\n")
            

        elif retrieval_algorithm == "Okapi BM25":
            results_bm25 = self.search_papers_okapi_bm25(search_query)
            for paper, score in results_bm25:
                print(f"Score: {score:.4f}")
                for key, value in self.dataset[paper].items():
                    print(f"'{key}': '{value}'")
                print("\n")
    


    # ------ Βήμα 4.β.1 Boolean retrieval ------
    # ------ Βήμα 4.δ. Επεξεργασία ερωτήματος (Query Processing) ------
    # Σειράς προτεραιότητας πράξεων: [1] -> [2] -> [3] -> [4] -> [5]
    def search_papers_boolean_retrieval(self, query):
        res = []
        terms = replace_terms_with_docs(query, self.inverted_index)
        while len(terms) > 1:
            if '(' and ')' in terms:                                            # [1] Εντοπίζονται οι πράξεις μέσα στις παρενθέσεις από αριστερά προς τα δεξιά
                start = terms.index('(')
                end = terms.index(')')
                subterms = terms[start + 1:end]
                while (len(subterms) > 1):
                    if 'not' in subterms:                                       # [2] Εκτελούνται οι πράξεις με τον τελεστή not από αριστερά προς τα δεξιά 
                        not_index = subterms.index('not')
                        not_query = subterms[not_index:not_index+2]
                        res = query_processing(not_query, len(self.dataset))
                        subterms[not_index] = res 
                        subterms.pop(not_index + 1)
                    else:
                        and_or_query = subterms[0:3]                            # [3] Εκτελούνται οι πράξεις με τους τελεστές and ή or από αριστερά προς τα δεξιά
                        res = query_processing(and_or_query, len(self.dataset))
                        subterms[0] = res 
                        subterms.pop(1)
                        subterms.pop(1) 
                terms[start] = [num for sublist in subterms for num in sublist]
                del terms[start + 1:end + 1]
            else:
                if 'not' in terms:                                              # [4] Δεν υπάρχουν παρενθέσεις άρα, εκτελούνται οι πράξεις με τον τελεστή not από αριστερά προς τα δεξιά
                    not_index = terms.index('not')
                    not_query = terms[not_index:not_index + 2]
                    res = query_processing(not_query, len(self.dataset))
                    terms[not_index] = res 
                    terms.pop(not_index + 1)
                else:                                                           # [5] Εκτελούνται οι πράξεις με τους τελεστές and και or από αριστερά προς τα δεξιά
                    and_or_query = terms[0:3]
                    res = query_processing(and_or_query, len(self.dataset))
                    terms[0] = res 
                    terms.pop(1)
                    terms.pop(1)        

        return res
    
    # ------ Βήμα 4.β.2 Vector Space Model (VSM) ------
    # ------ Βήμα 4.ε. Κατάταξη αποτελεσμάτων (Ranking) ------
    def search_papers_vector_space_model(self, query):                     
        tfidf_docs, idf_docs = calculate_tfidf_docs(self.dataset)
        tfidf_query = calculate_tfidf_query(query, idf_docs)

        cosine_similarities = [calculate_cosine_similarity(tfidf_query, doc) for doc in tfidf_docs]

        return rank_documents_vsm(self.dataset, cosine_similarities) 


    # ------ Βήμα 4.β.3 Probabilistic retrieval models (Okabi BM25) ------
    # ------ Βήμα 4.ε. Κατάταξη αποτελεσμάτων (Ranking) ------
    def search_papers_okapi_bm25(self, query):
        okapi_bm25_scores = []
        for doc in self.preprocessed_dataset:
           doc['score'] = self.calculate_okapi_bm25_score(query, doc['abstract'])
           okapi_bm25_scores.append(doc) 

        return rank_documents_bm25(okapi_bm25_scores) 
    
    def calculate_okapi_bm25_score(self, query, doc, k = 1.2, b = 0.75):
        score = 0
        # ------ Υπολογισμός μεγέθους εργασιών ------
        doc_length = len(doc)
    
        # ------ Υπολογισμός μέσου όρου μεγέθους συλλογής εργασιών ------
        total_docs = len(self.inverted_index.keys())
        total_doc_length = sum([len(doc) for doc in self.inverted_index.values()])
        average_doc_length = total_doc_length / total_docs
    
        # ------ Υπολογισμός TF-IDF κάθε όρου του ερωτήματος ------
        for term in query:
            if term in self.inverted_index:
                doc_frequency = len(self.inverted_index[term])
                inverse_doc_frequency = math.log((total_docs - doc_frequency + 0.5) / (doc_frequency + 0.5))
            
                # ------ Υπολογισμός TF που εμφανίζεται ο όρος του ερωτήματος στην συλλογή ------
                term_frequency = doc.count(term)
            
                # ------ Υπολογισμός BM25 συντελεστή για κάθε όρο του ερωτ΄΄ηματος ------
                score += inverse_doc_frequency * ((term_frequency * (k + 1)) / (term_frequency + k * (1 - b + b * (doc_length / average_doc_length))))
    
        return score
    
                 
        



