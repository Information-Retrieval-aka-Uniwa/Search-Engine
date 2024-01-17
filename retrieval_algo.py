def search_papers_bool(query, inverted_index):
    
    terms = query.lower().split()  # Μετατροπή του ερωτήματος αναζήτησης σε πεζά γράμματα και διαχωρισμός του σε λεκτικές μονάδες
    matching_papers = []           # Αρχικοποίηση της λίστας με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης              

    for i, term in enumerate(terms):

        if term == "and" and i > 0 and i < len(terms) - 1:
            previous_term = terms[i - 1]
            next_term = terms[i + 1]
            if previous_term in inverted_index and next_term in inverted_index:
                documents_with_previous_term = inverted_index[previous_term]
                
                for document in documents_with_previous_term:
                    if document in documents_with_next_term:
                        matching_papers.append(document)
                documents_with_next_term = inverted_index[next_term]

                for document in documents_with_next_term:
                    if document in documents_with_previous_term:
                        matching_papers.append(document)

        elif term == "or" and i > 0 and i < len(terms) - 1:
            previous_term = terms[i - 1]
            next_term = terms[i + 1]
            if previous_term in inverted_index or next_term in inverted_index:
                documents_with_previous_term = inverted_index[previous_term]
                for document in documents_with_previous_term:
                    if document in documents_with_next_term:
                        matching_papers.append(document)
                documents_with_next_term = inverted_index[next_term]
                
                for document in documents_with_next_term:
                    if document in documents_with_previous_term:
                        matching_papers.append(document)

        elif term == "not" and i < len(terms) - 1:
            next_term = terms[i + 1]
            if next_term not in inverted_index:
                documents = inverted_index[next_term]    
                for document in documents:           
                    matching_papers.append(document) 

    matching_papers = set(matching_papers) 
    
    return matching_papers
