import requests
from bs4 import BeautifulSoup

from web_crawler import web_scrape
from web_crawler import store_json
from text_processing import process_text

""""""""""""""""""""""""""""""""""""""""""""" 
 
    Βήμα 1. Σταχυολογητής (Web Crawler)
 
"""""""""""""""""""""""""""""""""""""""""""""
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

