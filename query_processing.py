def query_processing(query, inverted_index, dataset):
    terms = query.lower().split()
    boolean_retrieval_results = []
    for i, term in enumerate(terms):
        if term == "and" and i > 0 and i < len(terms) - 1:
            previous_term = terms[i - 1]
            next_term = terms[i + 1]
            docs_with_previous_term = []
            docs_with_next_term = []

            if previous_term in inverted_index:
                docs_with_previous_term = inverted_index[previous_term]
                for doc in docs_with_previous_term:
                    boolean_retrieval_results.append(doc)
            if next_term in inverted_index:
                docs_with_next_term = inverted_index[next_term]
                for doc in docs_with_next_term:
                    boolean_retrieval_results.append(doc)

            if (len(docs_with_previous_term) > 0 and len(docs_with_next_term) > 0):
                boolean_retrieval_results = sorted(set(docs_with_previous_term) & set(docs_with_next_term))
            elif len(docs_with_previous_term) > 0:
                boolean_retrieval_results = set(docs_with_previous_term)
            elif len(docs_with_next_term) > 0:
                boolean_retrieval_results = set(docs_with_next_term)

        elif term == "or" and i > 0 and i < len(terms) - 1:
            previous_term = terms[i - 1]
            next_term = terms[i + 1]
            docs_with_previous_term = []
            docs_with_next_term = []
            if previous_term in inverted_index:
                docs_with_previous_term = inverted_index[previous_term]
                for doc in docs_with_previous_term:
                    boolean_retrieval_results.append(doc)
            if next_term in inverted_index:
                docs_with_next_term = inverted_index[next_term]
                for doc in docs_with_next_term:
                    boolean_retrieval_results.append(doc)

            if (len(docs_with_previous_term) > 0 and len(docs_with_next_term) > 0):
                boolean_retrieval_results = sorted(set(docs_with_previous_term) | set(docs_with_next_term))
            elif len(docs_with_previous_term) > 0:
                boolean_retrieval_results = set(docs_with_previous_term)
            elif len(docs_with_next_term) > 0:
                boolean_retrieval_results = set(docs_with_next_term)

        elif term == "not" and i < len(terms) - 1:
            next_term = terms[i + 1]

            if next_term in inverted_index:
                docs_with_next_term = inverted_index[next_term]
                all_docs = set(range(len(dataset)))
                boolean_retrieval_results = sorted(all_docs - set(docs_with_next_term))

    return boolean_retrieval_results