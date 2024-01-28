import json
import random

from web_crawler import web_crawling
from text_preprocessing import preprocess_text
from inverted_index import create_inverted_index
from search_engine import SearchEngine


try:
    """"""""""""""""""""""""""""""""""""""""""""" 
 
        Βήμα 1. Σταχυολογητής (Web Crawler)
 
    """""""""""""""""""""""""""""""""""""""""""""
    """
    # ------ Δημιουργία του dataset ------
    subjects = ['Physics', 'Mathematics', 'Computer', 'Biology', 'Finance', 'Statistics', 'Electronics', 'Economics']
    num_subjects = random.randint(2, len(subjects))
    random_subjects = random.sample(subjects, num_subjects)
    # ------ Βήμα 1.α. Επιλογή ιστοτόπου-στόχου -----
    # ------ Βήμα 1.β. Υλοποίηση web crawler ------
    documents = web_crawling(random_subjects)
    # ------ Βήμα 1.γ. Αποθήκευση δεδομένων σε δομημένη μορφή  ------
    with open('dataset.json', 'w') as dataset:
        json.dump(documents, dataset, indent=4)
    """

    """"""""""""""""""""""""""""""""""""""""""""" 
    
        Βήμα 2. Προεπεξεργασία κειμένου (Text processing)
   
    """""""""""""""""""""""""""""""""""""""""""""
    # ------ Προεπεξεργασία του κειμενικού περιεχομένου του dataset ------
    with open('dataset.json', 'r') as file:
        dataset = json.load(file)

    for doc in dataset:
        doc['abstract'] = preprocess_text('abstract', doc.get('abstract'))
    
      
    """"""""""""""""""""""""""""""""""""""""""""" 
    
        Βήμα 3. Ευρετήριο (Indexing)
    
    """""""""""""""""""""""""""""""""""""""""""""
    # ------ Βήμα 3.α. Δημιουργία της ανεστραμμένης δομής δεδομένων ευρετηρίου ------
    # ------ Βήμα 3.β. Αποθήκευση της ανεστραμμένης δομής δεδομένων ευρετηρίου ------
    inverted_index = create_inverted_index(dataset)
    for key, value in inverted_index.items():
        print(f"{key} --> {value}")

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
   # se.init_gui()


except Exception as ex: 
    print("=================== Εξαίρεση ===================")
    print(str(ex))
