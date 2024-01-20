import nltk
import string
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

"""
Βήμα 2. Προεπεξεργασία κειμένου (Text Processing)

def process_text(text)

Είσοδος[1] --> [text]            Το κειμενικό περιεχόμενο που θα προεπεξεργαστεί 
Λειτουργία -->                   Υλοποίηση διάφορων τεχνικών προεπεξεργασίας κειμένου  (Tokenization --> Normalization --> Stemming --> Stop words removal)
Έξοδος[1]  --> [processed_text]  Το προεπεξεργασμένο κειμενικό περιεχόμενο
    
"""
def preprocess_list_of_texts(key, dataset):
    preprocessed_data = []
    for doc in dataset:
        preprocessed_data.append(preprocess_text(key, doc))
    return preprocessed_data

def preprocess_text(key, dataset):
    # ----- Tokenization -----
    tokens = word_tokenize(dataset)      # Χωρισμός του κειμένου σε λεκτικές μονάδες με χρήση της nltk.word_tokenize() για τον χωρισμό και των σημείων στίξης

    # ----- Punctuation characters removal -----
    string_punctuation = list(string.punctuation)  
    punctuation_tokens = [token for token in tokens if token not in string_punctuation] # Λίστα με όλες τις λέξεις που δεν ανήκουν στην λίστα με όλα τα σημεία στίξης
    
    # ----- Special characters removal -----
    special_text = re.sub(r'[^a-zA-Z0-9\s]', '', ' '.join(punctuation_tokens))
    special_tokens = special_text.split()

    # ----- Normalization -----
    normal_tokens = [token.lower() for token in special_tokens] # Αντικατάσταση όλων των κεφαλαίων γραμμάτων με πεζά

    # ----- Stop words removal -----
    stop_words = nltk.corpus.stopwords.words('english')                                     # Οι απαγορευμένες λέξεις της nltk.corpus.stopwords μεταβλητής με όρισμα τα αγγλικά (english) σε μία λίστα
    stop_tokens = [word for word in normal_tokens if word.lower() not in stop_words] # Λίστα με όλες τις λέξεις που δεν ανήκουν στην λίστα με όλες τις απαγορευμένες αγγλικές λέξεις και των σημείων στίξης

    if key == 'abstract':
        # ----- Stemming -----
        porter_stemmer = PorterStemmer()                                             # Εκτέλεση του αλγορίθμου του Porter για stemming
        stemmed_tokens = [porter_stemmer.stem(token) for token in stop_tokens] # Λίστα με όλες τις λέξεις που έχουν υποστεί αφαίρεση καταλήξεων και διατήρηση του κύριου στελέχους 
        return ' '.join(stemmed_tokens)
    else:
        return ' '.join(stop_tokens)
    

    

"""
def preprocess_text(text):
    
    preprocessed_tokens = preprocess_tokens(text)

    preprocessed_text = ' '.join(normalized_tokens)                        # Συνένωση των λέξεων της λίστας stop_words_removal_tokens ως ένα string για την τελική μορφή του προεπεξεργασμένου κείμενου

  
    return preprocessed_text


def preprocess_abstract(text):
    
    normalized_tokens = preprocess_tokens(text)

    # ----- Stemming -----
    porter_stemmer = PorterStemmer()                                             # Εκτέλεση του αλγορίθμου του Porter για stemming
    stemmed_tokens = [porter_stemmer.stem(token) for token in normalized_tokens] # Λίστα με όλες τις λέξεις που έχουν υποστεί αφαίρεση καταλήξεων και διατήρηση του κύριου στελέχους 
         
    processed_text = ' '.join(stemmed_tokens)                                    # Συνένωση των λέξεων της λίστας stop_words_removal_tokens ως ένα string για την τελική μορφή του προεπεξεργασμένου κείμενου
    processed_text = re.sub(r'[^a-zA-Z0-9\s]', '', processed_text)
  
    return processed_text
"""