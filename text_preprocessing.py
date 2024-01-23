""""""""""""""""""""""""""""""""""""""""""""" 
    
    Βήμα 2. Προεπεξεργασία κειμένου (Text processing)
   
"""""""""""""""""""""""""""""""""""""""""""""
import string
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

def preprocess_list_of_texts(key, dataset):
    preprocessed_data = []
    for doc in dataset:
        preprocessed_data.append(preprocess_text(key, doc))
    return preprocessed_data

def preprocess_text(key, dataset):
    # ------ Βήμα 2.β. Επιλογή τεχνικών προεπεξεργασίας κειμένου ------
    # ------ Tokenization ------
    tokens = word_tokenize(dataset)

    # ------ Punctuation characters removal ------
    string_punctuation = list(string.punctuation)
    punctuation_tokens = [token for token in tokens if token not in string_punctuation]

    # ------ Special characters removal ------
    special_text = re.sub(r'[^a-zA-Z0-9\s]', '', ' '.join(punctuation_tokens))
    special_tokens = special_text.split()

    # ------ Normalization ------
    normal_tokens = [token.lower() for token in special_tokens]

    # ------ Stopwords removal ------
    stop_words = stopwords.words('english')
    stop_tokens = [word for word in normal_tokens if word.lower() not in stop_words]
    # ------ Μόνο για τα πεδία abstract και του ερωτήματος χρήστη ------
    if key == 'abstract':
        # ------ Stemming ------
        porter_stemmer = PorterStemmer()
        stemmed_tokens = [porter_stemmer.stem(token) for token in stop_tokens]
        return ' '.join(stemmed_tokens)
    else:
        return ' '.join(stop_tokens)

    
