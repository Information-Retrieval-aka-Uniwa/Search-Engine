import tkinter 
from tkinter import ttk

def init_gui(papers, inverted_dict):
    # Create the main window
    window = tkinter.Tk()
    window.title("Αναζήτηση ακαδημαϊκών εργασιών")

    # Increase the window width
    window.geometry("400x200")

    # Create the search input field
    search_entry = tkinter.Entry(window, width=50)
    search_entry.pack(pady=10)

    # Create the search button
    def get_query():
        search_query = search_entry.get()
        print_papers(search_query, papers, inverted_dict)

    search_button = tkinter.Button(window, text="Αναζήτηση", command=get_query)
    search_button.pack()

    # Create the combobox
    options = ["Boolean Retrieval", "Vector Space Model", "Okapi BM25"]
    
    combobox = ttk.Combobox(window, values=options, state="readonly", width=30)
    combobox.set("Επιλογή αλγόριθμου ανάκτησης")  # Set the initial state to "Επιλογή αλγόριθμου ανάκτησης"
    combobox.pack()

    # Start the main event loop
    window.mainloop()

       
def search_papers(query, inverted_index):
    terms = query.lower().split()
    matching_abstracts = []

    for term in terms:
        if term in inverted_index:
            documents = inverted_index[term]
            for document in documents:
                matching_abstracts.append(document)  # Append the document number instead of the abstract

    matching_abstracts = list(set(matching_abstracts))
    
    return matching_abstracts  # Return the list of matching document numbers


def print_papers(search_query, papers, inverted_dict):

    returned_docs = []

    returned_docs = search_papers(search_query, inverted_dict) # Κλήση της συνάρτησης search για την αναζήτηση των εργασιών που περιέχουν το ερώτημα αναζήτησης

    print("Οι εργασίες που περιέχουν το ερώτημα αναζήτησης είναι : \n")
    for doc in returned_docs:
        paper = papers[doc]  # Get the abstract using the document number
        print("Title:", paper.get("title"))
        print("Authors:", paper.get("authors"))
        print("Subjects:", paper.get("subjects"))
        print("Comments:", paper.get("comments"))
        print("Abstract:", paper.get("abstract"))
        print("Date:", paper.get("date"))
        print("PDF URL:", paper.get("pdf_url"), "\n\n")

