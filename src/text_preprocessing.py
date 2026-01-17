""""""""""""""""""""""""""""""""""""""""""""" 
    
    Step 2. Text preprocessing
   
"""""""""""""""""""""""""""""""""""""""""""""
import string
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


def preprocess_text(key, dataset):
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

    # ------ Stop-words removal ------
    if key != 'boolean query':
        stop_words = stopwords.words('english')
        stop_tokens = [word for word in normal_tokens if word.lower() not in stop_words]
    else:
        stop_tokens = normal_tokens

    # ------ Stemming ------
    porter_stemmer = PorterStemmer()
    stemmed_tokens = [porter_stemmer.stem(token) for token in stop_tokens]
    
    return ' '.join(stemmed_tokens)
    
    # ------ Lemmatization ------
   # lemmatizer = WordNetLemmatizer()
   # lemmatized_tokens = [lemmatizer.lemmatize(token) for token in stop_tokens]
 
   # return ' '.join(lemmatized_tokens)    
    


    
