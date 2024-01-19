import json
import tkinter 
from tkinter import ttk

from retrieval_algos import search_papers_boolean, search_papers_default, search_papers_vector_space
import tkinter
from tkinter import ttk

"""
Βήμα 4. Μηχανή αναζήτησης (Search engine)

def init_gui(papers, inverted_dict)

Είσοδος[1] --> [papers]          Λίστα με τα δεδομένα κάθε εργασίας δομημένα σε μία δομή λεξικού με κλειδία τα ονόματα των δεδομένων και αντίστοιχα περιεχόμενα τα δεδομένα    
Είσοδος[2] --> [inverted_index]  Ανεστραμμένη δομή δεδομένων ευρετηρίου αποθηκευμένη σε μία δομή λεξικού 
Λειτουργία -->                   Αρχικοποίηση της διεπαφής χρήστη για την αναζήτηση εργασιών 
    
"""
"""
Βήμα 4. Μηχανή αναζήτησης (Search engine)

def print_papers(search_query, papers, inverted_dict)

Είσοδος[1] --> [search_query]    Ερώτημα αναζήτησης που εισήγαγε ο χρήστης στην διεπαφή χρήστη
Είσοδος[2] --> [papers]          Λίστα με τα δεδομένα κάθε εργασίας δομημένα σε μία δομή λεξικού με κλειδία τα ονόματα των δεδομένων και αντίστοιχα περιεχόμενα τα δεδομένα    
Είσοδος[3] --> [inverted_index]  Ανεστραμμένη δομή δεδομένων ευρετηρίου αποθηκευμένη σε μία δομή λεξικού 
Λειτουργία -->                   Εκτύπωση των ακαδημαϊκών εργασιών που περιέχουν το ερώτημα αναζήτησης 
    
"""

class SearchEngine:
    def __init__(self, json_data, json_preprocessed_data, inverted_index):
        with open(json_data, 'r') as file:
            self.data = json.load(file)
        with open(json_preprocessed_data, 'r') as file:
            self.preprocessed_data = json.load(file)
        self.inverted_index = inverted_index


    def init_gui(self):
        # ----- Παράθυρο διεπαφής χρήστη -----
        window = tkinter.Tk()                          # Αρχικοποίηση του παραθύρου της διεπαφής χρήστη
        window.title("Αναζήτηση ακαδημαϊκών εργασιών") # Ορισμός του τίτλου του παραθύρου
        window.geometry("400x200")                     # Ορισμός του μεγέθους του παραθύρου

        # ----- Πεδίο εισαγωγής κειμένου -----
        search_entry = tkinter.Entry(window, width=50) # Ορισμός του πλάτους του πεδίου εισαγωγής κειμένου
        search_entry.pack(pady=10)                     # Ορισμός του πεδίου εισαγωγής κειμένου στο παράθυρο

        # ----- Πεδίο επιλογής αλγορίθμου ανάκτησης -----
        options = ["Boolean Retrieval", "Vector Space Model", "Okapi BM25"]         # Ορισμός των επιλογών του πεδίου επιλογής αλγορίθμου ανάκτησης    
        combobox = ttk.Combobox(window, values=options, state="readonly", width=30) # Ορισμός του πλάτους του πεδίου επιλογής αλγορίθμου ανάκτησης, των επιλογών του πεδίου επιλογής αλγορίθμου ανάκτησης, της κατάστασης του πεδίου επιλογής αλγορίθμου ανάκτησης (readonly) και της δημιουργίας του πεδίου επιλογής αλγορίθμου ανάκτησης
        combobox.set("Επιλογή Αλγορίθμου Ανάκτησης")                                # Ορισμός της προεπιλεγμένης επιλογής του πεδίου επιλογής αλγορίθμου ανάκτησης
        combobox.pack()                                                             # Ορισμός του πεδίου επιλογής αλγορίθμου ανάκτησης στο παράθυρο

        # ----- Ερώτημα αναζήτησης (query) -----
        def get_query():                                        # Inline συνάρτηση που επιστρέφει το query που εισήγαγε ο χρήστης στην διεπαφή χρήστη
            search_query = search_entry.get()                   # Το query που εισήγαγε ο χρήστης στην διεπαφή χρήστη
            retrieval_algorithm = combobox.get()                 # Επιλεγμένος αλγόριθμος ανάκτησης
            print("Selected Algorithm:", retrieval_algorithm)    # Εκτύπωση του επιλεγμένου αλγορίθμου ανάκτησης
            self.print_papers(search_query, retrieval_algorithm)  # Κλήση της print_papers για την εκτύπωση των δεδομένων των εργασιών που περιέχουν το ερώτημα αναζήτησης

        # ----- Κουμπί αναζήτησης -----
        search_button = tkinter.Button(window, text="Αναζήτηση", command=get_query) # Ορισμός του κουμπιού αναζήτησης και κλήση της inline συνάρτησης get_query, όταν πατηθεί το κουμπί
        search_button.pack()                                                        # Ορισμός του κουμπιού αναζήτησης στο παράθυρο

        # ----- Εκτέλεση του παραθύρου -----
        window.mainloop()

    def print_papers(self, search_query, retrieval_algorithm):
        returned_docs = []

        if retrieval_algorithm == "Boolean Retrieval":
            returned_docs = search_papers_boolean(search_query, self.inverted_index, len(self.data))
        elif retrieval_algorithm == "Vector Space Model":
            returned_docs = search_papers_vector_space(search_query, self.data, self.preprocessed_data)
        elif retrieval_algorithm == "Okapi BM25":
            print('Okapi') # returned_docs = search_papers_okapi_bm25(search_query, self.json_data, self.preprocessed_json_data)

        print("Οι εργασίες που περιέχουν το ερώτημα αναζήτησης είναι: \n")
        """
        for doc in returned_docs:
            paper = self.data[doc]

            print("Id       : ", paper.get("id"))
            print("Title    : ", paper.get("title"))
            print("Authors  : ", paper.get("authors"))
            print("Subjects : ", paper.get("subjects"))
            print("Comments : ", paper.get("comments"))
            print("Abstract : ", paper.get("abstract"))
            print("Date     : ", paper.get("date"))
            print("PDF URL  : ", paper.get("pdf_url"), "\n\n")
        """



