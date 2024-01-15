
def search(query, inverted_index, abstracts):
    terms = query.lower().split()
    matching_abstracts = []

    for term in terms:
        if term in inverted_index:
            documents = inverted_index[term]
            for document in documents:
                matching_abstracts.append(document)  # Append the document number instead of the abstract

    matching_abstracts = list(set(matching_abstracts))
    return matching_abstracts  # Return the list of matching document numbers
