import json

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