import json
import tkinter
import nltk 
from tkinter import ttk

#from retrieval_algos import search_papers_boolean, search_papers_default, search_papers_vector_space
import tkinter
from tkinter import ttk
from query_processing import query_processing

from text_preprocessing import preprocess_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
import math

from web_crawler import web_crawling

class SearchEngine:

    def __init__(self, inverted_index):
        with open('dataset/dataset.json', 'r') as file:
            self.dataset = json.load(file)               
        with open('dataset/preprocessed_dataset.json', 'r') as file:
            self.preprocessed_dataset = json.load(file)
        self.inverted_index = inverted_index      

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
            print("Selected Algorithm:", retrieval_algorithm)  
            self.search_papers(search_query, retrieval_algorithm)  

        # ----- Κουμπί αναζήτησης -----
        search_button = tkinter.Button(window, text="Αναζήτηση", command=get_query)
        search_button.pack()                                                       

        # ----- Εκτέλεση του παραθύρου -----
        window.mainloop()

    def search_papers(self, search_query, retrieval_algorithm):
        if retrieval_algorithm == "Boolean Retrieval":
            results_boolean = self.search_papers_boolean_retrieval(search_query)
            print(results_boolean)
        elif retrieval_algorithm == "Vector Space Model":
            results_vsm = self.search_papers_vector_space_model(search_query)
            for paper, similarity in results_vsm:
                print(f"Similarity: {similarity:.4f}\n{paper}\n")
        elif retrieval_algorithm == "Okapi BM25":
            results_bm25 = self.search_papers_okapi_bm25(search_query)
            for paper, score in results_bm25:
                print(f"Score: {score:.4f}\n{paper}\n")

    def search_papers_boolean_retrieval(self, query):
        boolean_stack = self.create_boolean_stack(query)
        for boolean_query in boolean_stack:
            results_boolean = query_processing(boolean_query, self.inverted_index, self.dataset)


    def replace_terms_with_docs(self, query):
        terms = word_tokenize(query.lower())
        for term in terms:
            if term in self.inverted_index:
                if term != 'not' and term != 'and' and term != 'or' and term != '(' and term != ')':
                    docs_term = self.inverted_index[term]
                    terms[terms.index(term)] = docs_term

        return terms

    def create_boolean_stack(self, terms):
        res = []
        while len(terms) > 1:
            if '(' and ')' in terms:
                start = terms.index('(')
                end = terms.index(')')
                subterms = terms[start + 1:end]
                while (len(subterms) > 1):
                    if 'not' in subterms:
                        not_index = subterms.index('not')
                        not_query = subterms[not_index:not_index+2]
                        res = query_processing(not_query, self.dataset)
                        subterms[not_index] = res 
                        subterms.pop(not_index + 1)
                    else:
                        and_or_query = subterms[0:3]
                        res = query_processing(and_or_query, self.dataset)
                        subterms[0] = res 
                        subterms.pop(1)
                        subterms.pop(1) 
                terms[start] = [num for sublist in subterms for num in sublist]
                del terms[start + 1:end + 1]
            else:
                if 'not' in terms:
                    not_index = terms.index('not')
                    not_query = terms[not_index:not_index+2]
                    res = query_processing(not_query, self.dataset)
                    terms[not_index] = res 
                    terms.pop(not_index + 1)
                else:
                    and_or_query = terms[0:3]
                    res = query_processing(and_or_query, self.dataset)
                    terms[0] = res 
                    terms.pop(1)
                    terms.pop(1)        

        return res
    
    
    def search_papers_vector_space_model(self, query):
        vector_space_model_results = []
        # Step 1: Tokenize and preprocess the text
        tokenized_query = nltk.word_tokenize(preprocess_text('query', query))                      
        doc_id = [doc['doc_id'] for doc in self.dataset]                                              
        #title = [doc['title'] for doc in papers]
        preprocessed_abstracts = [doc['abstract'] for doc in self.preprocessed_dataset]        
        tokenized_abstracts = [nltk.word_tokenize(doc) for doc in preprocessed_abstracts]    

        # Step 2: Calculate TF-IDF
        # Convert tokenized documents to text
        preprocessed_abstracts = [' '.join(paper) for paper in tokenized_abstracts]          
        preprocessed_query = ' '.join(tokenized_query)                                      

        # Create a TF-IDF vectorizer
        tfidf_vectorizer = TfidfVectorizer()                                                
        tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_abstracts)               

        # Transform the query into a TF-IDF vector
        query_vector = tfidf_vectorizer.transform([preprocessed_query])                

        # Step 3: Calculate cosine similarity
        cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)                 

        # Step 4: Rank documents by similarity
        vector_space_model_results = [(doc_id[i], cosine_similarities[0][i]) for i in range(len(doc_id))]      
        vector_space_model_results.sort(key=lambda x: x[1], reverse=True)                                       

        return vector_space_model_results

    def search_papers_okapi_bm25(self, query):
        okapi_bm_25_results = []
        for doc in self.preprocessed_dataset:
           doc['score'] = self.calculate_okapi_bm25_score(query, doc['abstract'])
           okapi_bm_25_results.append(doc)
        okapi_bm_25_results.sort(key=lambda x: x['score'], reverse=True)
        okapi_bm_25_results = [(doc['doc_id'], doc['score']) for doc in okapi_bm_25_results]  
        
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
    
                 
        



