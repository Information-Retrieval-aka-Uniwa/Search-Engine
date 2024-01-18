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
def process_text(text):
    
    # ----- Tokenization -----
    tokens = word_tokenize(text)      # Χωρισμός του κειμένου σε λεκτικές μονάδες με χρήση της nltk.word_tokenize() για τον χωρισμό και των σημείων στίξης

    # ----- Stop words removal -----
    stop_words = nltk.corpus.stopwords.words('english')                                     # Οι απαγορευμένες λέξεις της nltk.corpus.stopwords μεταβλητής με όρισμα τα αγγλικά (english) σε μία λίστα
    string_punctuation = list(string.punctuation)                                           # Όλα τα σημεία στίξης σε μία λίστα
    stop_words = stop_words + string_punctuation                                            # Μία λίστα με όλες τις απαγορευμένες αγγλικές λέξεις και των σημείων στίξης
    stop_words_removal_tokens = [word for word in tokens if word.lower() not in stop_words] # Λίστα με όλες τις λέξεις που δεν ανήκουν στην λίστα με όλες τις απαγορευμένες αγγλικές λέξεις και των σημείων στίξης

    # ----- Normalization -----
    normalized_tokens = [token.lower() for token in stop_words_removal_tokens] # Αντικατάσταση όλων των κεφαλαίων γραμμάτων με πεζά

    # ----- Stemming -----
    porter_stemmer = PorterStemmer()                                             # Εκτέλεση του αλγορίθμου του Porter για stemming
    stemmed_tokens = [porter_stemmer.stem(token) for token in normalized_tokens] # Λίστα με όλες τις λέξεις που έχουν υποστεί αφαίρεση καταλήξεων και διατήρηση του κύριου στελέχους 
         
    processed_text = ' '.join(stemmed_tokens)                                    # Συνένωση των λέξεων της λίστας stop_words_removal_tokens ως ένα string για την τελική μορφή του προεπεξεργασμένου κείμενου
    processed_text = re.sub(r'[^a-zA-Z0-9\s]', '', processed_text)
  
    return processed_text