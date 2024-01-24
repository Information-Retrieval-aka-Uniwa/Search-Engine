""""""""""""""""""""""""""""""""""""""""""""" 
    
    Βήμα 4. Μηχανή αναζήτησης (Search engine)
    
"""""""""""""""""""""""""""""""""""""""""""""
import json
import tkinter

from tkinter import ttk
from query_processing import query_processing, replace_terms_with_docs
from ranking import calculate_cosine_similarity, calculate_okapi_bm25_score, calculate_tfidf_docs, calculate_tfidf_query, rank_documents_vsm, rank_documents_bm25



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
            print(f"============ Ερώτημα αναζήτησης: {search_query} ============")          
            print(f"----------- Αλγόριθμος ανάκτησης: {retrieval_algorithm} -----------")
            print(f"Τα αποτελέσματα αναζήτησης αποθηκεύτηκαν στο αρχείο results\\{retrieval_algorithm} Results.txt\n") 
            self.search_papers(search_query, retrieval_algorithm)  

        # ----- Κουμπί αναζήτησης -----
        search_button = tkinter.Button(window, text="Αναζήτηση", command=get_query)
        search_button.pack()                                                       

        # ----- Εκτέλεση του παραθύρου -----
        window.mainloop()

    # ------ Βήμα 4.β. Υλοποίηση αλγορίθμων ανάκτησης ------
    def search_papers(self, search_query, retrieval_algorithm):
        
        if retrieval_algorithm == "Boolean Retrieval":
            results_boolean = self.search_papers_boolean_retrieval(search_query)
            with open('results/Boolean Retrieval Results.txt', 'w', encoding='utf-8') as results_boolean_file:
                results_boolean_file.write(f"============ Ερώτημα αναζήτησης: {search_query} ============\n")
                i = 1
                for doc_id in results_boolean:
                    results_boolean_file.write('--------------------------------------------------\n')
                    results_boolean_file.write(f"#{i}\n")
                    results_boolean_file.write('--------------------------------------------------\n')
                    for key, value in self.dataset[doc_id].items():
                        if key == 'doc_id':
                            results_boolean_file.write(f"Document ID: {value}\n")
                        elif key == 'title':
                            results_boolean_file.write(f"Title: {value}\n")
                        elif key == 'authors':
                            results_boolean_file.write(f"Authors: {value}\n")
                        elif key == 'subjects':
                            results_boolean_file.write(f"Subjects: {value}\n")
                        elif key == 'abstract':
                            results_boolean_file.write(f"Abstract: {value}\n")
                        elif key == 'comments':
                            results_boolean_file.write(f"Comments: {value}\n")
                        elif key == 'date':
                            results_boolean_file.write(f"Date: {value}\n")
                        elif key == 'pdf_url':
                            results_boolean_file.write(f"PDF_URL: {value}\n")
                    results_boolean_file.write("\n")
                    i += 1
        
        elif retrieval_algorithm == "Vector Space Model":
            results_vsm = self.search_papers_vector_space_model(search_query)
            with open('results/Vector Space Model Results.txt', 'w', encoding='utf-8') as results_vsm_file:
                results_vsm_file.write(f"============ Ερώτημα αναζήτησης: {search_query} ============\n")
                i = 1
                for doc, score in results_vsm:
                    results_vsm_file.write('--------------------------------------------------\n')
                    results_vsm_file.write(f"#{i} Cosine Similarity: {score:.2f}\n")
                    results_vsm_file.write('--------------------------------------------------\n')
                    results_vsm_file.write(f"Document ID: {doc['doc_id']}\n")
                    results_vsm_file.write(f"Title: {doc['title']}\n")
                    results_vsm_file.write(f"Authors: {doc['authors']}\n")
                    results_vsm_file.write(f"Subjects: {doc['subjects']}\n")
                    results_vsm_file.write(f"Abstract: {doc['abstract']}\n")
                    results_vsm_file.write(f"Comments: {doc['comments']}\n")
                    results_vsm_file.write(f"Date: {doc['date']}\n")
                    results_vsm_file.write(f"PDF_URL: {doc['pdf_url']}\n")
                    results_vsm_file.write("\n")
                    i += 1            

        elif retrieval_algorithm == "Okapi BM25":
            results_bm25 = self.search_papers_okapi_bm25(search_query)
            with open('results/Okapi BM25 Results.txt', 'w', encoding='utf-8') as results_bm25_file:
                results_bm25_file.write(f"============ Ερώτημα αναζήτησης: {search_query} ============\n")
                i = 1
                for doc_id, score in results_bm25:
                    results_bm25_file.write('--------------------------------------------------\n')
                    results_bm25_file.write(f"#{i} BM25 Score: {score:.2f}\n")
                    results_bm25_file.write('--------------------------------------------------\n')
                    for key, value in self.dataset[doc_id].items():
                        if key == 'doc_id':
                            results_bm25_file.write(f"Document ID: {value}\n")
                        elif key == 'title':
                            results_bm25_file.write(f"Title: {value}\n")
                        elif key == 'authors':
                            results_bm25_file.write(f"Authors: {value}\n")
                        elif key == 'subjects':
                            results_bm25_file.write(f"Subjects: {value}\n")
                        elif key == 'abstract':
                            results_bm25_file.write(f"Abstract: {value}\n")
                        elif key == 'comments':
                            results_bm25_file.write(f"Comments: {value}\n")
                        elif key == 'date':
                            results_bm25_file.write(f"Date: {value}\n")
                        elif key == 'pdf_url':
                            results_bm25_file.write(f"PDF_URL: {value}\n")
                    results_bm25_file.write("\n")
                    i += 1
    

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
        
        tfidf_docs, idf_docs = calculate_tfidf_docs(self.preprocessed_dataset)
        tfidf_query = calculate_tfidf_query(query, idf_docs)
        cosine_similarities = [calculate_cosine_similarity(tfidf_query, doc) for doc in tfidf_docs]

        return rank_documents_vsm(self.dataset, cosine_similarities) 


    # ------ Βήμα 4.β.3 Probabilistic retrieval models (Okabi BM25) ------
    # ------ Βήμα 4.ε. Κατάταξη αποτελεσμάτων (Ranking) ------
    def search_papers_okapi_bm25(self, query):
        
        okapi_bm25_scores = []
        for doc in self.dataset:
           doc['score'] = calculate_okapi_bm25_score(query, self.inverted_index, doc['abstract'])
           okapi_bm25_scores.append(doc) 

        return rank_documents_bm25(okapi_bm25_scores) 
    

    
                 
        



