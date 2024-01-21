import json
import random

from web_crawler import web_crawling
from text_preprocessing import preprocess_list_of_texts, preprocess_text
from inverted_index import create_inverted_index
from search_engine import SearchEngine


try:
    """"""""""""""""""""""""""""""""""""""""""""" 
 
        Βήμα 1. Σταχυολογητής (Web Crawler)
 
    """""""""""""""""""""""""""""""""""""""""""""
    # ------ Δημιουργία του dataset ------
    subjects = ['Physics', 'Mathematics', 'Computer Science', 'Quantitative Biology', 'Quantitative Finance', 'Statistics', 'Electrical Engineering and Systems Science', 'Economics']
    num_subjects = random.randint(1, len(subjects))
    random_subjects = random.sample(subjects, num_subjects)
    # ------ Βήμα 1.α. Επιλογή ιστοτόπου-στόχου -----
    # ------ Βήμα 1.β. Υλοποίηση web crawler ------
    documents = web_crawling(random_subjects)
    # ------ Βήμα 1.γ. Αποθήκευση δεδομένων σε δομημένη μορφή  ------
    with open('dataset/dataset.json', 'w') as f:
        json.dump(documents, f, indent=4)
 

    """"""""""""""""""""""""""""""""""""""""""""" 
    
        Βήμα 2. Προεπεξεργασία κειμένου (Text processing)
   
    """""""""""""""""""""""""""""""""""""""""""""
    # ------ Προεπεξεργασία του dataset ------
    with open('dataset/dataset.json', 'r') as file:
        dataset = json.load(file)
    # ------ Βήμα 2.α. Επιλογή εργασιών προεπεξεργασίας κειμένου ------
    # ------ Βήμα 2.β. Αιτιολόγηση επιλογής εργασιών ------
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
    # ------ Βήμα 2.γ. Αποθήκευση προεπεξεργασμένων δεδομένων σε δομημένη μορφή  ------
    with open('dataset/preprocessed_dataset.json', 'w') as f:
        json.dump(preprocessed_docs, f, indent=4)


    """"""""""""""""""""""""""""""""""""""""""""" 
    
        Βήμα 3. Ευρετήριο (Indexing)
    
    """""""""""""""""""""""""""""""""""""""""""""
    # ------ Βήμα 3.α. Δημιουργία της ανεστραμμένης δομής δεδομένων ευρετηρίου ------
    with open('dataset/preprocessed_dataset.json', 'r') as file:
        preprocessed_data = json.load(file)
    # ------ Βήμα 3.β. Αποθήκευση της ανεστραμμένης δομής δεδομένων ευρετηρίου ------
    inverted_index = create_inverted_index(preprocessed_data)
    with open('dataset/inverted_index.txt', 'w') as file2:
        for key, value in inverted_index.items():
            file2.write(f"{key} --> {value}\n")
    

    """"""""""""""""""""""""""""""""""""""""""""" 
    
        Βήμα 4. Μηχανή αναζήτησης (Search engine)
    
    """""""""""""""""""""""""""""""""""""""""""""
    # ------ Βήμα 4.α Ανάπτυξη διεπαφής χρήστη για αναζήτηση εργασιών ------
    # ------ Βήμα 4.β. Υλοποίηση αλγορίθμων ανάκτησης ------
    # ------ Βήμα 4.β.1 Boolean retrieval ------
    # ------ Βήμα 4.β.2 Vector Space Model (VSM) ------
    # ------ Βήμα 4.β.3 Probabilistic retrieval models (Okabi BM25) ------
    # ------ Βήμα 4.γ. Φιλτράρισμα αποτελεσμάτων αναζήτησης με διάφορα κριτήρια ------
    # ------ Βήμα 4.δ. Επεξεργασία ερωτήματος (Query Processing) ------
    # ------ Βήμα 4.ε. Κατάταξη αποτελεσμάτων (Ranking) ------
    se = SearchEngine(inverted_index)
    se.init_gui()

except Exception as ex: 
    print("_____________________Εξαίρεση_____________________")
    print(str(ex))
