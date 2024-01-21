def query_processing(terms, dataset):
    for i, term in enumerate(terms):
        if term == "and":
            docs_with_previous_term = terms[i - 1]
            docs_with_next_term = terms[i + 1]
            boolean_retrieval_results = sorted(set(docs_with_previous_term) & set(docs_with_next_term))

        elif term == "or":
            docs_with_previous_term = terms[i - 1]
            docs_with_next_term = terms[i + 1]
            boolean_retrieval_results = sorted(set(docs_with_previous_term) | set(docs_with_next_term))
    
        elif term == "not":
            docs_with_next_term = terms[i + 1]
            all_docs = set(range(len(dataset)))
            boolean_retrieval_results = sorted(all_docs - set(docs_with_next_term))

    return boolean_retrieval_results



