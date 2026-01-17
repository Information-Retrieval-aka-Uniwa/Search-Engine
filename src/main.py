import json
import random

from web_crawler import web_crawling
from text_preprocessing import preprocess_text
from inverted_index import create_inverted_index
from search_engine import SearchEngine


try:
    """"""""""""""""""""""""""""""""""""""""""""" 
    
    Step 1. Web Crawler

    """""""""""""""""""""""""""""""""""""""""""""
    
    # ------ Dataset creation ------
    subjects = ['Physics', 'Mathematics', 'Computer', 'Biology', 'Finance', 'Statistics', 'Electronics', 'Economics']
    num_subjects = random.randint(2, len(subjects))
    random_subjects = random.sample(subjects, num_subjects)
    
    # ------ Step 1.a. Target website selection ------
    # ------ Step 1.b. Web crawler implementation ------
    documents = web_crawling(random_subjects)
    
    # ------ Step 1.c. Store data in structured format ------
    with open('dataset.json', 'w') as dataset:
        json.dump(documents, dataset, indent=4)
    

    """"""""""""""""""""""""""""""""""""""""""""" 
        
        Step 2. Text Preprocessing

    """""""""""""""""""""""""""""""""""""""""""""
    
    # ------ Preprocess the textual content of the dataset ------
    with open('dataset.json', 'r') as file:
        dataset = json.load(file)

    for doc in dataset:
        doc['abstract'] = preprocess_text('abstract', doc.get('abstract'))
    
      
    """"""""""""""""""""""""""""""""""""""""""""" 
        
        Step 3. Indexing

    """""""""""""""""""""""""""""""""""""""""""""
    
    # ------ Step 3.a. Creation of the inverted index data structure ------
    # ------ Step 3.b. Storage of the inverted index data structure ------
    inverted_index = create_inverted_index(dataset)

    """"""""""""""""""""""""""""""""""""""""""""" 
        
        Step 4. Search Engine

    """""""""""""""""""""""""""""""""""""""""""""
    
    # ------ Step 4.a. Development of a user interface for paper search ------
    # ------ Step 4.b. Implementation of retrieval algorithms ------
    # ------ Step 4.c. Filtering search results using various criteria ------
    # ------ Query Processing ------
    # ------ Result Ranking ------
    se = SearchEngine(inverted_index)
    se.init_gui()


except Exception as ex: 
    print("=================== Exception ===================")
    print(str(ex))
