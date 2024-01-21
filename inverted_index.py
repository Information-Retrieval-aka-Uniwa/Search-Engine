def create_inverted_index(preprocessed_dataset, key):

    if key == 'title' or key == 'abstract' or key == 'date':
        inverted_index = {}
        for doc in preprocessed_dataset:
            text = doc.get(key)
            terms = text.split()
            for term in terms:
                if term not in inverted_index:
                    inverted_index[term] = set()
                inverted_index[term].add(doc['doc_id'])

        inverted_index = dict(sorted(inverted_index.items()))
        for term in inverted_index:
            inverted_index[term] = sorted(inverted_index[term])

        with open('dataset/inverted_index.txt', 'w') as file2:
           for key, value in inverted_index.items():
            file2.write(f"{key} --> {value}\n")

    return inverted_index





       


