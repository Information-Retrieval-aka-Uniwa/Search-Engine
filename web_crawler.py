import json
import requests

from bs4 import BeautifulSoup
import json
import requests
from bs4 import BeautifulSoup

"""
Βήμα 1. Σταχυολογητής (Web Crawler)

def web_scrape(soup, max_limit)

Είσοδος[1] --> [soup]      Το έγγραφο HTML της σελίδας που έχει τις σελίδες με URL https://arxiv.org/abs/XXXX.XXXXX που αντιστοιχεί σε εργασία με τα δεδομένα της (τίτλος, συγγραφείς, μαθήματα, σχόλια, περίληψη, ημερομηνία δημοσίευσης, url λήψης του pdf της εργασίας)
Είσοδος[2] --> [max_limit] Το μέγιστο πλήθος των εργασιών όπου θέλουμε να συλλέξουμε τα δεδομένα τους από την εκάστοτε σελίδα με URL https://arxiv.org/abs/XXXX.XXXXX
Λειτουργία -->             Ανάλυση των εγγράφων HTML με URL https://arxiv.org/abs/XXXX.XXXXX για την συλλογή δεδομένων (Web Scraping) εργασιών 
Έξοδος[1]  --> [papers]    Λίστα με τα δεδομένα κάθε εργασίας δομημένα σε μία δομή λεξικού (data) με κλειδία τα ονόματα των δεδομένων και αντίστοιχα περιεχόμενα τα δεδομένα    
    
"""
def web_crawling(random_subjects):
    dataset = []
    doc_id = 0
    for sub in random_subjects:
        url = 'https://arxiv.org/search/?query=' + sub + '&searchtype=all&source=header&size=100'
        page = requests.get(url)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, 'html.parser')
        for elements in soup.find_all('li', class_='arxiv-result'):
            # --- Τίτλος ---
            title = elements.find('p', class_='title is-5 mathjax').text.strip()
            # --- Συγγραφείς ---
            authors = elements.find('p', class_='authors').text.strip().removeprefix("Authors:").split(", ")
            authors = [author.strip() for author in authors]
            # --- Μαθήματα ---
            subjects = []
            for subject in elements.find_all('span'):
                if subject.get('data-tooltip') is not None:
                    subjects.append(subject.get('data-tooltip')) 
            # --- Περίληψη ---
            abstract = elements.find('span', class_='abstract-full has-text-grey-dark mathjax').text.strip().removeprefix("Abstract:").removesuffix("\n        \u25b3 Less")
            abstract = abstract.strip()
            # --- Σχόλια ---
            has_comments = elements.find('p', class_='comments is-size-7')
            if has_comments is None:
                comments = ' '
            else:
                comments = has_comments.text.strip().removeprefix("Comments:").replace("\n", "")
            # --- Ημερομηνία δημοσίευσης ---
            date = elements.find('p', class_='is-size-7').text.strip().removeprefix("Submitted ").split(";")[0]
            # --- URL λήψης του pdf της εργασίας ---
            for pdf_link in elements.find_all('a'):                     
                pdf_href = pdf_link.get('href')                       
                if pdf_href and pdf_href.startswith('https://arxiv.org/pdf/'):         
                    pdf_url = pdf_href 
            data = {
                'doc_id'   : doc_id,
                'title'    : title,
                'authors'  : authors,
                'subjects' : subjects,
                'abstract' : abstract,
                'comments' : comments,
                'date'     : date,
                'pdf_url'  : pdf_url
            }
            doc_id = doc_id + 1
            dataset.append(data)

    return dataset    

    """
    tokens_query = query.split()
    url = 'https://arxiv.org/search/?query=' + '+'.join(tokens_query) + '&searchtype=all&source=header&size=100'
    page = requests.get(url)
    page.raise_for_status()
    soup = BeautifulSoup(page.text, 'html.parser')
    """
    """
    papers = []
    id = 0                                                                                                 # Αρχικοποίηση της λίστας με τα δεδομένα κάθε εργασίας
    for link in soup.find_all('a'):                                                                         # Αναζήτηση όλων των ετικέτων <a> από το έγγραφο HTML της σελίδας 
        href = link.get('href')                                                                             # Εκχώρηση του περιεχομένου των ετικέτων <a> που ξεκινάνε με 'href' σε μία μεταβλητή
        if href and href.startswith('/abs/'):                                                               # Το περιεχόμενο υπάρχει και ξεκινάει με την συμβολοσειρά '/abs/' (περιεχόμενο με ετικέτα href='/abs/XXXX.XXXXX' που αντιστοιχεί σε εργασία με τα δεδομένα της)
            abs_url = 'https://arxiv.org/' + href                                                           # Συγχώνευση του περιεχομένου '/abs/XXXX.XXXXX' με το 'https://arxiv.org/' για τον σχηματισμό του URL της σελίδας με τα δεδομένα της εργασίας
            abs_page = requests.get(abs_url)                                                                # Φόρτωση της web σελίδας https://arxiv.org/abs/XXXX.XXXXX μέσω HTTP-GET
            abs_page.raise_for_status()                                                                     # Σε περίπτωση επιστροφής κωδικού πέρα από το 200 (OK), πέταξε εξαίρεση
            abs_soup = BeautifulSoup(abs_page.text, 'html.parser')                                          # Ανάλυση του εγγράφου HTML από την αναζήτηση της σελίδας (Web Crawling) με URL https://arxiv.org/abs/XXXX.XXXXX
            element = abs_soup.find('div', id='abs')                                                        # Αναζήτηση των δεδομένων της εργασίας
            if element:                                                                                     # Υπάρχει η ετικέτα <div> με id="abs"
                if len(papers) < max_limit:                                                                 # Οι εργασίες που θα συλλέγξουμε τα δεδομένα (Web Scraping) δεν ξεπερνάνε το μέγιστο πλήθος των εργασιών που ορίσαμε στην Είσοδο[2]
                    title = element.find('h1', class_='title mathjax').text.strip().removeprefix("Title:")  # Συλλογή του τίτλου της εργασίας
                    authors = element.find('div', class_='authors').text.strip().removeprefix("Authors:")   # Συλλογή των συγγραφέων της εργασίας
                    subjects = element.find('td', class_='tablecell subjects').text.strip()                 # Συλλογή των μαθημάτων της εργασίας
                    hasComment = element.find('td', class_='tablecell comments mathjax')                    # Αναζήτηση σχολίων στην εργασία
                    if hasComment is not None:                                                              # Υπάρχουν σχόλια στην εργασία
                        comments = hasComment.text.strip()                                                  # Συλλογή των σχόλιων της εργασίας
                    else:                                                                                   # Δεν υπάρχουν σχόλια στην εργασία
                        comments = ' '                                                                      # Κενή συμβολοσειρά για την δήλωση απουσίας σχολίων στην εργασία
                    abstract = element.find('blockquote', class_='abstract mathjax').text.strip().removeprefix("Abstract:")      # Συλλογή της περίληψης της εργασίας
                    date = element.find('div', class_='dateline').text.strip().removeprefix("[Submitted on ").removesuffix("]")  # Συλλογή της ημερομηνίας δημοσίευσης
                    for pdf_link in abs_soup.find_all('a'):                      # Αναζήτηση του συνδέσμου για την λήψη του PDF της εργασίας
                        pdf_href = pdf_link.get('href')                          # Εκχώρηση του περιεχομένου των ετικέτων <a> που ξεκινάνε με 'href' σε μία μεταβλητή
                        if pdf_href and pdf_href.startswith('/pdf/'):            # Έλεγχος αν υπάρχει το pdf_href και αν ξεκινά με τη συμβολοσειρά '/pdf/'
                            pdf_url = 'https://arxiv.org/' + pdf_href            # Σχηματισμός του URL για τη λήψη του PDF της εργασίας
                    # Αποθήκευση των δεδομένων της εργασίας σε μία δομή λεξικού
                    data = {
                        'id'   : id,
                        'title': title,
                        'authors': authors,
                        'subjects': subjects,
                        'comments': comments,
                        'abstract': abstract,
                        'date': date,
                        'pdf_url': pdf_url
                    }
                    id = id + 1
                    papers.append(data) # Αποθήκευση του λεξικού με τα δεδομένα της εργασίας σε μία λίστα
                else:                   # Οι εργασίες που θα συλλέγξουμε τα δεδομένα (Web Scraping) ξεπερνάνε το μέγιστο πλήθος των εργασιών που ορίσαμε στην Είσοδο[2]
                    break               # Σταματάμε την συλλογή δεδομένων


    return papers # Επιστροφή της λίστας με τα δεδομένα κάθε εργασίας
    """

"""
Βήμα 1. Σταχυολογητής (Web Crawler)

def store_json(papers)

Είσοδος[1] --> [papers]     Λίστα με τα δεδομένα κάθε εργασίας δομημένα σε μία δομή λεξικού με κλειδία τα ονόματα των δεδομένων και αντίστοιχα περιεχόμενα τα δεδομένα     
Λειτουργία -->              Αποθήκευση των δεδομένων των εργασιών σε δομημένη μορφή JSON 
Έξοδος[1]  --> [json_data]  Τα δεδομένα κάθε εργασιάς ως μία δομημένη μορφή JSON
    
"""
def store_json(papers, json_name):
    json_data = json.dumps(papers, indent=4)
    with open(json_name, 'w') as file:
        file.write(json_data)


