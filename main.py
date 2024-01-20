import json
import requests
from bs4 import BeautifulSoup

from web_crawler import web_crawling, store_json 
from text_preprocessing import preprocess_list_of_texts, preprocess_text
from inverted_index import create_inverted_index
from search_engine import SearchEngine
import random


try:
    """"""""""""""""""""""""""""""""""""""""""""" 
 
        Βήμα 1. Σταχυολογητής (Web Crawler)
 
    """""""""""""""""""""""""""""""""""""""""""""
    subjects = ['Physics', 'Mathematics', 'Computer Science', 'Quantitative Biology', 'Quantitative Finance', 'Statistics', 'Electrical Engineering and Systems Science', 'Economics']

    num_subjects = random.randint(1, len(subjects))
    random_subjects = random.sample(subjects, num_subjects)
    print(random_subjects)

    random_subject = ['Statistics']
    documents = web_crawling(random_subject)

    store_json(documents, 'dataset.json')


    """"""""""""""""""""""""""""""""""""""""""""" 
    
        Βήμα 2. Προεπεξεργασία κειμένου (Text processing)
   
    """""""""""""""""""""""""""""""""""""""""""""
    with open('dataset.json', 'r') as file:
        dataset = json.load(file)

    preprocessed_docs = []   
    for doc in dataset:
        preprocessed_data = {
            'doc_id'    : doc.get('doc_id'),
            'title'     : preprocess_text('title', doc.get('title')),
            'authors'   : preprocess_list_of_texts('authors', doc.get('authors')),
            'subjects'  : preprocess_list_of_texts('subjects', doc.get('subjects')),
            'abstract'  : preprocess_text('abstract', doc.get('abstract')),
            'comments'  : preprocess_text('comments', doc.get('comments')),
            'date'      : preprocess_text('date', doc.get('date')),
            'pdf_url'   : doc.get('pdf_url')
        }
        preprocessed_docs.append(preprocessed_data)

    store_json(preprocessed_docs, 'preprocessed_dataset.json')
    

    """"""""""""""""""""""""""""""""""""""""""""" 
    
        Βήμα 3. Ευρετήριο (Indexing)
    
    """""""""""""""""""""""""""""""""""""""""""""
    with open('preprocessed_dataset.json', 'r') as file:
        preprocessed_data = json.load(file)

    inverted_index = create_inverted_index(preprocessed_data)
    with open('inverted_index.txt', 'w') as file2:
        for key, value in inverted_index.items():
            file2.write(f"{key} --> {value}\n")
 

    """"""""""""""""""""""""""""""""""""""""""""" 
    
        Βήμα 4. Μηχανή αναζήτησης (Search engine)
    
    """""""""""""""""""""""""""""""""""""""""""""
    se = SearchEngine(inverted_index)
    se.init_gui()
      
    
except Exception as ex: 
    print("_____________________Εξαίρεση_____________________")
    print(str(ex))
