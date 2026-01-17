""""""""""""""""""""""""""""""""""""""""""""" 
    
    Step 4. Search Engine
    
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

             

    # ------ Step 4.α Development of user interface for searching papers ------
    def init_gui(self):
        # ----- User interface window -----
        window = tkinter.Tk()                      
        window.title("Search of academic papers")
        window.geometry("400x200")                   

        # ----- Entry field for user query -----
        search_entry = tkinter.Entry(window, width=50) 
        search_entry.pack(pady=10)                 

        # ----- Entry field for selecting retrieval algorithm -----
        options = ["Boolean Retrieval", "Vector Space Model", "Probabilistic Retrieval Model"]           
        combobox = ttk.Combobox(window, values=options, state="readonly", width=30) 
        combobox.set("Select Retrieval Algorithm")                                
        combobox.pack()                                                            

        # ----- User query -----
        def get_query():                                     
            search_query = search_entry.get()                    
            self.retrieval_algorithm = combobox.get()
            print("\n")
            print(f"============ User Query   : {search_query} ============")          
            print(f"============ Retrieval Algorithm : {self.retrieval_algorithm} ============")
            self.search_papers(search_query)  

        # ----- Search button for results of the retrieval algorithm -----
        search_button = tkinter.Button(window, text="Search", command=get_query)
        search_button.pack()


        # ----- Entry field for filtering criteria -----
        search_entry2 = tkinter.Entry(window, width=50) 
        search_entry2.pack(pady=10)  

        # ----- Entry field for selecting filter -----
        options = ["Authors", "Date"]           
        combobox2 = ttk.Combobox(window, values=options, state="readonly", width=30) 
        combobox2.set("Select Filter")                                
        combobox2.pack()


        # ----- Select Filter -----
        def get_filter():
            filtering_query = search_entry2.get()
            filter = combobox2.get()
            print("\nFiltering results by: " + filter)
            self.filtering(filter, filtering_query)
                                                             
        # ----- Search button for results of the filtering -----
        filter_button = tkinter.Button(window, text="Search", command=get_filter)
        filter_button.pack()                                                       

        # ----- Execution of the window -----
        window.mainloop()

    # ------ Step 4.β. Implementation of retrieval algorithms ------
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
    # ------ Query Processing ------
    # Priority order of operations: [1] -> [2] -> [3] -> [4] -> [5]
    def search_papers_boolean_retrieval(self, query):
        
        res = []
        terms = replace_terms_with_docs(query, self.inverted_index)
        while len(terms) > 1:
            if '(' and ')' in terms:                                            # [1] Locate the operations within parentheses from left to right
                start = terms.index('(')
                end = terms.index(')')
                subterms = terms[start + 1:end]
                while (len(subterms) > 1):
                    if 'not' in subterms:                                       # [2] Operations with the not operator are performed from left to right. 
                        not_index = subterms.index('not')
                        not_query = subterms[not_index:not_index+2]
                        res = query_processing(not_query, len(self.dataset))
                        subterms[not_index] = res 
                        subterms.pop(not_index + 1)
                    else:
                        and_or_query = subterms[0:3]                            # [3] Operations with the operators and or are performed from left to right.
                        res = query_processing(and_or_query, len(self.dataset))
                        subterms[0] = res 
                        subterms.pop(1)
                        subterms.pop(1) 
                terms[start] = [num for sublist in subterms for num in sublist]
                del terms[start + 1:end + 1]
            else:
                if 'not' in terms:                                              # [4] There are no parentheses, so operations with the not operator are performed from left to right.
                    not_index = terms.index('not')
                    not_query = terms[not_index:not_index + 2]
                    res = query_processing(not_query, len(self.dataset))
                    terms[not_index] = res 
                    terms.pop(not_index + 1)
                else:                                                           # [5] Operations with the operators and or are performed from left to right
                    and_or_query = terms[0:3]
                    res = query_processing(and_or_query, len(self.dataset))
                    terms[0] = res 
                    terms.pop(1)
                    terms.pop(1)        

        return res
    
    # ------ Vector Space Model (VSM) ------
    # ------ Ranking of results ------
    def search_papers_vector_space_model(self, query):                     
        
        tfidf_docs, idf_docs = calculate_tfidf_docs(self.dataset)
        tfidf_query = calculate_tfidf_query(query, idf_docs)
        cosine_similarities = [calculate_cosine_similarity(tfidf_query, doc) for doc in tfidf_docs]

        return rank_documents_vsm(self.dataset, cosine_similarities) 


    # ------ Probabilistic retrieval models (Okabi BM25) ------
    # ------ Ranking of results ------
    def search_papers_okapi_bm25(self, query):
        
        okapi_bm25_scores = []
        for doc in self.dataset:
           doc['score'] = calculate_okapi_bm25_score(query, self.inverted_index, doc['abstract'])
           okapi_bm25_scores.append(doc) 

        return rank_documents_bm25(okapi_bm25_scores) 


    # ------ Step 4.γ. Filtering search results with various criteria ------
    def filtering(self, filter, search_query):
        
        if filter == "Authors":
          
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

        elif filter == "Date":

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


           
                       
                         
        
            
     
        
    
                 
        



