import requests
from bs4 import BeautifulSoup

from web_crawler import web_scrape
from web_crawler import store_json
from text_processing import process_text
from inverted_index import create_inverted_index

try:
    """"""""""""""""""""""""""""""""""""""""""""" 
 
        Βήμα 1. Σταχυολογητής (Web Crawler)
 
    """""""""""""""""""""""""""""""""""""""""""""
    #------------------ Βήμα 1.α. Επιλογή ιστοτόπου-στόχου (arXiv) ------------------
    # Εισαγωγή του URL της σελίδας του μαθήματος που ενδιαφέρομαι για την αναζήτηση εργασιών
    # subject_url = input("Δώσε το url της σελίδας του μαθήματος : ") 
    subject_url = 'https://arxiv.org/list/astro-ph/recent'

    # Φόρτωση της web σελίδας μέσω HTTP-GET
    subject_page = requests.get(subject_url)
    # Σε περίπτωση επιστροφής κωδικού πέρα από το 200 (OK), πέταξε εξαίρεση
    subject_page.raise_for_status()

    #------------------ Βήμα 1.β. Υλοποίηση web crawler με BeautifulSoup ------------------
    # Ανάλυση του εγγράφου HTML από την αναζήτηση της σελίδας (Web Crawling) με URL subject_url
    subject_soup = BeautifulSoup(subject_page.text, 'html.parser')

    # Αρχικοποίηση της λίστας με τα URLs του μαθήματος που περιέχουν λίστα με συγκεκριμένο αριθμό εργασιών
    list_urls = []
            
    # Αναζήτηση όλων των ετικέτων <a> από το έγγραφο HTML της σελίδας με URL subject_url
    for link in subject_soup.find_all('a'):
        # Εκχώρηση του περιεχομένου των ετικέτων <a> που ξεκινάνε με 'href' σε μία μεταβλητή
        href = link.get('href')
        # Το περιεχόμενο υπάρχει και ξεκινάει με την συμβολοσειρά '/list/' (περιεχόμενο με ετικέτα href='/list/μορφότυπο_μαθήματος/' που αντιστοιχεί σε σελίδα με λίστα εργασιών)
        if href and href.startswith('/list/'):
            list_urls.append(href) # Αποθήκευση των περιεχομένων σε μία λίστα

    # Αναζήτηση της λίστας για το περιεχόμενο που περιλαμβάνει την λίστα με όλες τις εργασίες ενός μαθήματος
    all_papers_url = ' '
    for list_url in list_urls:
        # Έλεγχος αν πρόκειται για το περιεχόμενο που περιέχει την λίστα με όλες τις εργασίες ενός μαθήματος
        if "pastweek?show=" in list_url:
            all_papers_url = list_url # Αποθήκευση του περιεχομένου σε μία μεταβλητή

    # Αρχικοποίηση μίας λίστας για την αποθήκευση των δεδομένα κάθε εργασίας δομημένα σε μία δομή λεξικού με κλειδία τα ονόματα των δεδομένων και αντίστοιχα περιεχόμενα τα δεδομένα
    papers = []

    # Μέγιστος αριθμός των εργασιών, των οποίων θέλουμε να συλλέξουμε τα δεδομένα
    max_limit = 2

    # Υπάρχει περιεχόμενο που περιέχει την λίστα με όλες τις εργασίες ενός μαθήματος
    if "pastweek?show=" in all_papers_url:
        # Ολοκληρωμένη σύνταξη του URL που περιέχει την λίστα με όλες τις εργασίες 
        all_papers_url = 'https://arxiv.org' + all_papers_url
        
        # Φόρτωση της web σελίδας μέσω HTTP-GET
        all_papers_page = requests.get(all_papers_url)
        # Σε περίπτωση επιστροφής κωδικού πέρα από το 200 (OK), πέταξε εξαίρεση
        all_papers_page.raise_for_status()

        # Ανάλυση του εγγράφου HTML από την αναζήτηση της σελίδας (Web Crawling) με URL https://arxiv.org/list/όνομα_μαθήματος/list/recent/pastweek?show=αριθμός_εργασιών
        all_papers_soup = BeautifulSoup(all_papers_page.text, 'html.parser')    
        
        # Κλήση της συνάρτησης web_scrape για την συλλογή των δεδομένων των εργασιών με URL https://arxiv.org/list/όνομα_μαθήματος/recent/pastweek?show=αριθμός_εργασιών
        papers = web_scrape(all_papers_soup, max_limit)

    #------------------ Βήμα 1.γ. Αποθήκευση δεδομένων σε δομημένη μορφή (JSON) ------------------  
        # Κλήση της συνάρτησης store_json για την αποθήκευση των μεταδεδομένων σε JSON
        print("_____________________Βήμα 1. Σταχυολογητής (Web Crawler)_____________________") 
        json_data = store_json(papers)
        print('\n')
    # Δεν υπάρχει περιεχόμενο που περιέχει την λίστα με όλες τις εργασίες ενός μαθήματος
    else:
        # Κλήση της συνάρτησης web_scrape για την συλλογή των δεδομένων των εργασιών με URL https://arxiv.org/list/όνομα_μαθήματος/new
        papers = web_scrape(subject_soup, max_limit)

    #------------------ Βήμα 1.γ. Αποθήκευση δεδομένων σε δομημένη μορφή (JSON) ------------------    
        # Κλήση της συνάρτησης store_json για την αποθήκευση των δεδομένων σε JSON
        print("_____________________Βήμα 1. Σταχυολογητής (Web Crawler)_____________________")
        json_data = store_json(papers)
        print('\n')


    """"""""""""""""""""""""""""""""""""""""""""" 
    
        Βήμα 2. Προεπεξεργασία κειμένου (Text processing)
   
    """""""""""""""""""""""""""""""""""""""""""""
    #------------------ Βήμα 2.α. Επιλογή εργασιών προεπεξεργασίας κειμένου ------------------
    # Αρχικοποίηση της λίστας με τις προεπεξεργασμένες περιλήψεις (abstract) των εργασιών
    processed_abstracts = []
    # Προσπέλαση της λίστας με τα δεδομένα κάθε εργασίας δομημένα σε μία δομή λεξικού με κλειδία τα ονόματα των δεδομένων και αντίστοιχα περιεχόμενα τα δεδομένα  
    for data in papers:
        abstract = data.get('abstract')                      # Ανάκτηση του περιεχομένου του λεξικού με κλειδί 'abstract' 
        processed_abstracts.append(process_text(abstract))   # Κλήση της συνάρτησης process_text για την προεπεξεργασία της περίληψης της εργασίας και αποθήκευση στην λίστα processed_abstracts
    #------------------ Βήμα 2.β. Αιτιολόγηση επιλογής εργασιών ------------------
    # Εκτύπωση των προεπεξεργασμένων περιλήψεων (abstracts) των εργασιών
    print("_____________________Βήμα 2. Προεπεξεργασία κειμένου (Text processing)_____________________")
    for index, abstract in enumerate(processed_abstracts):
        print(f'---- Paper #{index + 1} ----')
        print(abstract)    
    print('\n')


    """"""""""""""""""""""""""""""""""""""""""""" 
    
        Βήμα 3. Ευρετήριο (Indexing)
    
    """""""""""""""""""""""""""""""""""""""""""""
    #------------------ Βήμα 3.α. Δημιουργία της ανεστραμμένης δομής δεδομένων ευρετηρίου ------------------
    # Κλήση της συνάρτησης create_inverted_index για την δημιουργία της ανεστραμμένης δομής δεδομένων ευρετηρίου
    inverted_dict = create_inverted_index(processed_abstracts)
    #------------------ Βήμα 3.β. Αποθήκευση του ευρετηρίου σε μία δομή δεδομένων ------------------
    # Εκτύπωση του ευρετηρίου
    print("_____________________Βήμα 3. Ευρετήριο (Indexing)_____________________")
    for key, value in inverted_dict.items():
        print(key, '-->', value)
    print('\n')


except Exception as ex: 
    print("_____________________Εξαίρεση_____________________")
    print(str(ex))
