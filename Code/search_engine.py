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
        with open("dataset.json", "r") as dataset:
            self.dataset = json.load(dataset)               
        self.inverted_index = inverted_index 
        self.results_boolean = []
        self.results_vsm = []
        self.results_bm25 = []
        self.retrieval_algorithm = ""

             

    # ------ Βήμα 4.α Ανάπτυξη διεπαφής χρήστη για αναζήτηση εργασιών ------
    def init_gui(self):
        # ----- Παράθυρο διεπαφής χρήστη -----
        window = tkinter.Tk()                      
        window.title("Αναζήτηση ακαδημαϊκών εργασιών")
        window.geometry("400x200")                   

        # ----- Πεδίο εισαγωγής ερωτήματος χρήστη -----
        search_entry = tkinter.Entry(window, width=50) 
        search_entry.pack(pady=10)                 

        # ----- Πεδίο επιλογής αλγορίθμου ανάκτησης -----
        options = ["Boolean Retrieval", "Vector Space Model", "Probabilistic Retrieval Model"]           
        combobox = ttk.Combobox(window, values=options, state="readonly", width=30) 
        combobox.set("Επιλογή Αλγορίθμου Ανάκτησης")                                
        combobox.pack()                                                            

        # ----- Ερώτημα αναζήτησης (query) -----
        def get_query():                                     
            search_query = search_entry.get()                    
            self.retrieval_algorithm = combobox.get()
            print("\n")
            print(f"============ Ερώτημα αναζήτησης   : {search_query} ============")          
            print(f"============ Αλγόριθμος ανάκτησης : {self.retrieval_algorithm} ============")
            self.search_papers(search_query)  

        # ----- Κουμπί αναζήτησης αποτελεσμάτων αλγόριθμου ανάκτησης -----
        search_button = tkinter.Button(window, text="Αναζήτηση", command=get_query)
        search_button.pack()


        # ----- Πεδίο εισαγωγής κριτηρίου φίλτρου -----
        search_entry2 = tkinter.Entry(window, width=50) 
        search_entry2.pack(pady=10)  

        # ----- Πεδίο επιλογής φιλτρου -----
        options = ["Συγγραφείς", "Ημερομηνία"]           
        combobox2 = ttk.Combobox(window, values=options, state="readonly", width=30) 
        combobox2.set("Επιλογή Φίλτρου")                                
        combobox2.pack()


        # ----- Επιλογή φίλτρου -----
        def get_filter():
            filtering_query = search_entry2.get()
            filter = combobox2.get()
            print("\nΦιλτράρισμα αποτελεσμάτων κατά: " + filter)
            self.filtering(filter, filtering_query)
                                                             
        # ----- Κουμπί αναζήτησης αποτελεσμάτων φίλτρου -----
        filter_button = tkinter.Button(window, text="Αναζήτηση", command=get_filter)
        filter_button.pack()                                                       

        # ----- Εκτέλεση του παραθύρου -----
        window.mainloop()

    # ------ Βήμα 4.β. Υλοποίηση αλγορίθμων ανάκτησης ------
    def search_papers(self, search_query):
        
        if self.retrieval_algorithm == "Boolean Retrieval":
            self.results_boolean = self.search_papers_boolean_retrieval(search_query)
            count_results = 0
            for doc_id in self.results_boolean:
                if count_results < 20:
                    doc = self.dataset[doc_id]
                    print('--------------------------------------------------')
                    print(f"#{count_results + 1}")
                    print('--------------------------------------------------')
                    print(f"Document ID : {doc['doc_id']}")
                    print(f"Title       : {doc['title']}")
                    print(f"Authors     : {', '.join(doc['authors'])}")
                    print(f"Subjects    : {', '.join(doc['subjects'])}")
                    print(f"Abstract    : {doc['abstract']}")
                    print(f"Comments    : {doc['comments']}")
                    print(f"Date        : {doc['date']}")
                    print(f"PDF_URL     : {doc['pdf_url']}")
                    count_results += 1
                else:
                    break

        elif self.retrieval_algorithm == "Vector Space Model":
            self.results_vsm = self.search_papers_vector_space_model(search_query)
            count_results = 0
            for doc, score in self.results_vsm:
                if count_results < 20:
                    print('--------------------------------------------------')
                    print(f"#{count_results + 1} Cosine Similarity: {score:.4f}")
                    print('--------------------------------------------------')
                    print(f"Document ID : {doc['doc_id']}")
                    print(f"Title       : {doc['title']}")
                    print(f"Authors     : {', '.join(doc['authors'])}")
                    print(f"Subjects    : {', '.join(doc['subjects'])}")
                    print(f"Abstract    : {doc['abstract']}")
                    print(f"Comments    : {doc['comments']}")
                    print(f"Date        : {doc['date']}")
                    print(f"PDF_URL     : {doc['pdf_url']}")
                    count_results += 1
                else:
                    break
       
        elif self.retrieval_algorithm == "Probabilistic Retrieval Model":
            self.results_bm25 = self.search_papers_okapi_bm25(search_query)
            count_results = 0
            for doc_id, score in self.results_bm25:
                if count_results < 20:
                    doc = self.dataset[doc_id]
                    print('--------------------------------------------------')
                    print(f"#{count_results + 1} BM25 Score: {score:.4f}")
                    print('--------------------------------------------------')
                    print(f"Document ID : {doc['doc_id']}")
                    print(f"Title       : {doc['title']}")
                    print(f"Authors     : {', '.join(doc['authors'])}")
                    print(f"Subjects    : {', '.join(doc['subjects'])}")
                    print(f"Abstract    : {doc['abstract']}")
                    print(f"Comments    : {doc['comments']}")
                    print(f"Date        : {doc['date']}")
                    print(f"PDF_URL     : {doc['pdf_url']}")
                    count_results += 1
                else:
                    break
    

    # ------ Boolean retrieval ------
    # ------ Επεξεργασία ερωτήματος (Query Processing) ------
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
    
    # ------ Vector Space Model (VSM) ------
    # ------ Κατάταξη αποτελεσμάτων (Ranking) ------
    def search_papers_vector_space_model(self, query):                     
        
        tfidf_docs, idf_docs = calculate_tfidf_docs(self.dataset)
        tfidf_query = calculate_tfidf_query(query, idf_docs)
        cosine_similarities = [calculate_cosine_similarity(tfidf_query, doc) for doc in tfidf_docs]

        return rank_documents_vsm(self.dataset, cosine_similarities) 


    # ------ Probabilistic retrieval models (Okabi BM25) ------
    # ------ Κατάταξη αποτελεσμάτων (Ranking) ------
    def search_papers_okapi_bm25(self, query):
        
        okapi_bm25_scores = []
        for doc in self.dataset:
           doc['score'] = calculate_okapi_bm25_score(query, self.inverted_index, doc['abstract'])
           okapi_bm25_scores.append(doc) 

        return rank_documents_bm25(okapi_bm25_scores) 


    # ------ Βήμα 4.γ. Φιλτράρισμα αποτελεσμάτων αναζήτησης με διάφορα κριτήρια ------
    def filtering(self, filter, search_query):
        
        if filter == "Συγγραφείς":
          
          if self.retrieval_algorithm == "Boolean Retrieval":
            count_results = 0
            for doc_id in self.results_boolean:
                if count_results < 20:
                    doc = self.dataset[doc_id]
                    if search_query in doc['authors']:
                        print('--------------------------------------------------')
                        print(f"#{count_results + 1}")
                        print('--------------------------------------------------')
                        print(f"Document ID : {doc['doc_id']}")
                        print(f"Title       : {doc['title']}")
                        print(f"Authors     : {', '.join(doc['authors'])}")
                        print(f"Subjects    : {', '.join(doc['subjects'])}")
                        print(f"Abstract    : {doc['abstract']}")
                        print(f"Comments    : {doc['comments']}")
                        print(f"Date        : {doc['date']}")
                        print(f"PDF_URL     : {doc['pdf_url']}")
                        count_results += 1
                else:
                    break
          
          elif self.retrieval_algorithm == "Vector Space Model":
            count_results = 0
            for doc, score in self.results_vsm:
                if count_results < 20:
                    if search_query in doc['authors']:
                        print('--------------------------------------------------')
                        print(f"#{count_results + 1} Cosine Similarity: {score:.4f}")
                        print('--------------------------------------------------')
                        print(f"Document ID : {doc['doc_id']}")
                        print(f"Title       : {doc['title']}")
                        print(f"Authors     : {', '.join(doc['authors'])}")
                        print(f"Subjects    : {', '.join(doc['subjects'])}")
                        print(f"Abstract    : {doc['abstract']}")
                        print(f"Comments    : {doc['comments']}")
                        print(f"Date        : {doc['date']}")
                        print(f"PDF_URL     : {doc['pdf_url']}")
                        count_results += 1
                else:
                    break
          
          elif self.retrieval_algorithm == "Probabilistic Retrieval Model":
            count_results = 0
            for doc_id, score in self.results_bm25:
                if count_results < 20:
                    doc = self.dataset[doc_id]
                    if search_query in doc['authors']:
                        print('--------------------------------------------------')
                        print(f"#{count_results + 1} BM25 Score: {score:.4f}")
                        print('--------------------------------------------------')
                        print(f"Document ID : {doc['doc_id']}")
                        print(f"Title       : {doc['title']}")
                        print(f"Authors     : {', '.join(doc['authors'])}")
                        print(f"Subjects    : {', '.join(doc['subjects'])}")
                        print(f"Abstract    : {doc['abstract']}")
                        print(f"Comments    : {doc['comments']}")
                        print(f"Date        : {doc['date']}")
                        print(f"PDF_URL     : {doc['pdf_url']}")
                        count_results += 1
                else:
                    break

        elif filter == "Ημερομηνία":

            if self.retrieval_algorithm == "Boolean Retrieval":
                count_results = 0
                for doc_id in self.results_boolean:
                    if count_results < 20:
                        doc = self.dataset[doc_id]
                        if search_query in doc['date']:
                            print('--------------------------------------------------')
                            print(f"#{count_results + 1}")
                            print('--------------------------------------------------')
                            print(f"Document ID : {doc['doc_id']}")
                            print(f"Title       : {doc['title']}")
                            print(f"Authors     : {', '.join(doc['authors'])}")
                            print(f"Subjects    : {', '.join(doc['subjects'])}")
                            print(f"Abstract    : {doc['abstract']}")
                            print(f"Comments    : {doc['comments']}")
                            print(f"Date        : {doc['date']}")
                            print(f"PDF_URL     : {doc['pdf_url']}")
                            count_results += 1
                    else:
                        break
            
            elif self.retrieval_algorithm == "Vector Space Model":
                count_results = 0
                for doc, score in self.results_vsm:
                    if count_results < 20:
                        if search_query in doc['date']:
                            print('--------------------------------------------------')
                            print(f"#{count_results + 1} Cosine Similarity: {score:.4f}")
                            print('--------------------------------------------------')
                            print(f"Document ID : {doc['doc_id']}")
                            print(f"Title       : {doc['title']}")
                            print(f"Authors     : {', '.join(doc['authors'])}")
                            print(f"Subjects    : {', '.join(doc['subjects'])}")
                            print(f"Abstract    : {doc['abstract']}")
                            print(f"Comments    : {doc['comments']}")
                            print(f"Date        : {doc['date']}")
                            print(f"PDF_URL     : {doc['pdf_url']}")
                            count_results += 1
                    else:
                        break
            
            elif self.retrieval_algorithm == "Probabilistic Retrieval Model":
                count_results = 0
                for doc_id, score in self.results_bm25:
                    if count_results < 20:
                        doc = self.dataset[doc_id]
                        if search_query in doc['date']:
                            print('--------------------------------------------------')
                            print(f"#{count_results + 1} BM25 Score: {score:.4f}")
                            print('--------------------------------------------------')
                            print(f"Document ID : {doc['doc_id']}")
                            print(f"Title       : {doc['title']}")
                            print(f"Authors     : {', '.join(doc['authors'])}")
                            print(f"Subjects    : {', '.join(doc['subjects'])}")
                            print(f"Abstract    : {doc['abstract']}")
                            print(f"Comments    : {doc['comments']}")
                            print(f"Date        : {doc['date']}")
                            print(f"PDF_URL     : {doc['pdf_url']}")
                            count_results += 1
                    else:
                        break    


           
                       
                         
        
            
     
        
    
                 
        



