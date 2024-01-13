import string
import requests
import nltk
from bs4 import BeautifulSoup
import json

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


""""""""""""""""""""""""""""""""""""""""""""" 
 
    Βήμα 1. Σταχυολογητής (Web Crawler)
 
"""""""""""""""""""""""""""""""""""""""""""""
def web_scrape(soup, elements, papers, max_limit):
    # Προσπέλαση κάθε στοιχείου (element) και συλλογή της επιθυμητής πληροφορίας
    for index, element in enumerate(elements):
        # Έλεγχος για το αν έχει ξεπεραστεί ο μέγιστος αριθμός των paper, των οποίων θέλω να συλλέξω τα μεταδεδομένα
        if len(papers) < max_limit:
            titles = [title.text.strip() + '\n' for title in element.find_all('div', class_='list-title mathjax')]                              # Τίτλος
            authors = [author.text.strip('Authors: ').replace('\n', ' ') + '\n' for author in element.find_all('div', class_='list-authors')]   # Συγγραφέας
            comments = [comment.text.strip() + '\n' for comment in element.find_all('div', class_='list-comments mathjax')]                     # Σχόλια
            subjects = [subject.text.strip() + '\n' for subject in element.find_all('div', class_='list-subjects')]                             # Μαθήματα
            date = soup.find('h3').text.strip()                                                                                                 # Ημερομηνία δημοσίευσης

            # Δημιουργία ενός λεξικού και αποθήκευση της πληροφορίας που συλλέγω για κάθε paper
            data = {
                'titles': titles,
                'authors': authors,
                'subjects': subjects,
                'comments': comments,
                'date published': date
                }
        
            # Αποθήκευση του λεξικού στην λίστα papers
            papers.append(data)
        else:
            break
    
    return papers

def store_json(papers):
    # Εκτύπωση των μεταδεδομένων κάθε paper ξεχωριστά
    for index, paper in enumerate(papers):
        print(f'\n--- Paper {index + 1} ---')
        for key, value in paper.items():
            if key == 'date published':
                print(f'{key}: {value}')  # Εκτύπωση της ημερομηνίας δημοσίευσης σε μία γραμμή
            else:
                for item in value:
                    print(item)
         # Εκτύπωση των μεταδεδομένων σε δομημένη μορφή JSON
        json_data = json.dumps(paper, indent=4)
        print(f'JSON Data:\n{json_data}')
    
    return json_data

#------------------ Βήμα 1α. Επιλογή ιστοτόπου-στόχου (arXiv) ------------------
# Εισαγωγή του URL της σελίδας του μαθήματος που ενδιαφέρομαι για τα paper
subject_url = input("Δώσε το url της σελίδας του μαθήματος : ")

# Φόρτωση της web σελίδας μέσω HTTP-GET
subject_page = requests.get(subject_url)

#------------------ Βήμα 1β. Υλοποίηση web crawler με BeautifulSoup ------------------
# Web crawling την πληροφορία της σελίδας μέσω μίας ένθετης δομής HTML
subject_soup = BeautifulSoup(subject_page.text, 'html.parser')

# Αρχικοποίηση της λίστας με τα URLs του μαθήματος που περιέχουν λίστα με συγκεκριμένο αριθμό paper
list_urls = []
           
# Προσπέλαση όλων των URL του HTML που εμπεριέχονται στη κεφαλίδα <a>
for link in subject_soup.find_all('a'):
    # Όλα τα URL της κεφαλίδας <a> που έχουν την παράμετρο href
    href = link.get('href')
    # Έλεγχος αν το URL της κεφαλίδας <a> έχει την παράμετρο href και ξεκινάει με '/list/'
    if href and href.startswith('/list/'):
        list_urls.append(href) # Αποθήκευση του URL στην λίστα

# Προσπέλαση όλων των URL που ξεκινάνε με '/list/' 
all_papers_url = ' '
for list_url in list_urls:
    # Έλεγχος αν πρόκειται για το URL που περιέχει όλα τα paper 
    if "pastweek?show=" in list_url:
        all_papers_url = list_url # Αποθήκευση του URL σε μία μεταβλητή

# Αρχικοποίηση μίας λίστας για την αποθήκευση των μεταδεδομένων των paper
papers = []

# Μέγιστος αριθμός των paper, των οποίων θέλω να συλλέξω τα μεταδεδομένα
max_limit = 100

# Έλεγχος για το αν υπάρχει όντως URL που περιέχει όλα τα paper, διαφορετικά κρατάμε το URL του μαθήματος
if "pastweek?show=" in all_papers_url:
    # Ολοκληρωμένη σύνταξη του URL που περιέχει όλα τα paper
    all_papers_url = 'https://arxiv.org' + all_papers_url
    
    # Φόρτωση της web σελίδας μέσω HTTP-GET
    all_papers_page = requests.get(all_papers_url)

    # Web crawling την πληροφορία της σελίδας μέσω μίας ένθετης δομής HTML
    all_papers_soup = BeautifulSoup(all_papers_page.text, 'html.parser')    

    # Αναζήτηση στο HTML του URL που περιέχει όλα τα paper, όλων των 'div' στοιχείων που έχουν την κλάση 'meta' 
    all_papers_elements = all_papers_soup.find_all('div', class_='meta')

    # Κλήση της συνάρτησης web_scrape για την συλλογή των μεταδεδομένων των paper
    papers = web_scrape(all_papers_soup, all_papers_elements, papers, max_limit)

#------------------ Βήμα 1γ. Αποθήκευση δεδομένων σε δομημένη μορφή (JSON) ------------------  
    # Κλήση της συνάρτησης store_json για την αποθήκευση των μεταδεδομένων σε JSON 
    json_data = store_json(papers)
else:
    # Αναζήτηση στο HTML του URL του μαθήματος, όλων των 'div' στοιχείων που έχουν την κλάση 'meta' 
    subject_elements = subject_soup.find_all('div', class_='meta')
    
    # Κλήση της συνάρτησης web_scrape για την συλλογή των μεταδεδομένων των paper
    papers = web_scrape(subject_soup, subject_elements, papers, max_limit)

#------------------ Βήμα 1γ. Αποθήκευση δεδομένων σε δομημένη μορφή (JSON) ------------------    
    # Κλήση της συνάρτησης store_json για την αποθήκευση των μεταδεδομένων σε JSON 
    json_data = store_json(papers)


""""""""""""""""""""""""""""""""""""""""""""" 
 
    Βήμα 2. Προεπεξεργασία κειμένου (Text processing)
 
"""""""""""""""""""""""""""""""""""""""""""""
def process_text(text):
    # Tokenization
    tokens = word_tokenize(text)

    # Normalization
    normalized_tokens = [x.lower() for x in tokens]

    # Stemming
    porter_stemmer = PorterStemmer()
    stemmed_tokens = [porter_stemmer.stem(token) for token in normalized_tokens]
    
    # Lemmatization
    wnl_lemmatize = nltk.WordNetLemmatizer()
    lemmatized_tokens = [wnl_lemmatize.lemmatize(token) for token in stemmed_tokens]
    
    # Stop words removal
    stop_words = nltk.corpus.stopwords.words('english')
    string_punctuation = list(string.punctuation)
    stop_words = stop_words + string_punctuation
    stop_words_removal_tokens = [word for word in lemmatized_tokens if word.lower() not in stop_words]
        
    # Join the tokens back into a string
    processed_text = ' '.join(stop_words_removal_tokens)
    
    return processed_text


sample_text = "This is a sample text for processing. It includes various words and different verb tenses."

processed_text = process_text(sample_text)

print("Original Text:")
print(sample_text)

print("\nProcessed Text:")
print(processed_text)

"""
proccesed_data = []
for data in json_data:
    proccesed_data.append(process_text(data))
print(proccesed_data)"""

