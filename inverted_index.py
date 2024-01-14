def create_inverted_index(documents):
    inverted_index = {}
    for doc_id, document in enumerate(documents):
        for word in document.split():
            if word not in inverted_index:
                inverted_index[word] = set()
            inverted_index[word].add(doc_id)
    return inverted_index


