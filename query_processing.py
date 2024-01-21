from nltk.tokenize import word_tokenize

def query_processing(terms, num_of_docs):
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
            all_docs = set(range(num_of_docs))
            boolean_retrieval_results = sorted(all_docs - set(docs_with_next_term))

    return boolean_retrieval_results

def replace_terms_with_docs(query, inverted_index):
    terms = word_tokenize(query.lower())
    for term in terms:
        if term != 'and' and term != 'or' and term != 'not' and term != '(' and term != ')': 
            if term in inverted_index:
                if term != 'not' and term != 'and' and term != 'or' and term != '(' and term != ')':
                    docs_term = inverted_index[term]
                    terms[terms.index(term)] = docs_term
            else:
                raise Exception("Term not found in the inverted index")

    return terms


