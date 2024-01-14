import nltk
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

def process_text(text):
    # Tokenization
    tokens = word_tokenize(text)

    # Normalization
    #  normalized_tokens = [x.lower() for x in tokens]

    # Stop words removal
    stop_words = nltk.corpus.stopwords.words('english')
    stop_words = nltk.corpus.stopwords.words('english')
    string_punctuation = list(string.punctuation)
    stop_words = stop_words + string_punctuation
    stop_words_removal_tokens = [word for word in tokens if word.lower() not in stop_words]

    # Stemming
    porter_stemmer = PorterStemmer()
    stemmed_tokens = [porter_stemmer.stem(token) for token in stop_words_removal_tokens]
    
    # Lemmatization
    # wnl_lemmatize = nltk.WordNetLemmatizer()
    # lemmatized_tokens = [wnl_lemmatize.lemmatize(token) for token in stop_words_removal_tokens]
    
    
        
    # Join the tokens back into a string
    processed_text = ' '.join(stemmed_tokens)
    
    return processed_text