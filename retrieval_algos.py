from collections import Counter, OrderedDict
import copy
import math
import nltk

from text_preprocessing import preprocess_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math
from collections import Counter

def search_papers_boolean(query, inverted_index, num_of_papers):
    terms = query.lower().split()  # Μετατροπή του ερωτήματος αναζήτησης σε πεζά γράμματα και διαχωρισμός του σε λεκτικές μονάδες
    matching_papers = []           # Αρχικοποίηση της λίστας με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης              
    for i, term in enumerate(terms):

        if term == "and" and i > 0 and i < len(terms) - 1:             # Έλεγχος για το αν ο όρος κλειδί (term) είναι "and" και αν βρίσκεται μεταξύ δύο όρων κλειδιών (terms)
            previous_term = terms[i - 1]                               # Αρχικοποίηση του προηγούμενου όρου κλειδιού (previous_term) από τον όρο κλειδί (term) που εξετάζουμε
            next_term = terms[i + 1]                                   # Αρχικοποίηση του επόμενου όρου κλειδιού (next_term) από τον όρο κλειδί (term) που εξετάζουμε
            documents_with_previous_term = []                          # Αρχικοποίηση της λίστας με τους αριθμούς των εργασιών που περιέχουν τον προηγούμενο όρο κλειδί (previous_term)
            documents_with_next_term = []                              # Αρχικοποίηση της λίστας με τους αριθμούς των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
            if previous_term in inverted_index:
                documents_with_previous_term = inverted_index[previous_term] # Ανάκτηση των αριθμών των εργασιών που περιέχουν τον προηγούμενο όρο κλειδί (previous_term)
                for document in documents_with_previous_term:                # Προσπέλαση των αριθμών των εργασιών που περιέχουν τον προηγούμενο όρο κλειδί (previous_term)
                    matching_papers.append(document)                         # Προσθήκη του αριθμού της εργασίας στη λίστα με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης
            if next_term in inverted_index:
                documents_with_next_term = inverted_index[next_term]         # Ανάκτηση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                for document in documents_with_next_term:                    # Προσπέλαση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                    matching_papers.append(document)                         # Προσθήκη του αριθμού της εργασίας στη λίστα με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης
            
            if (len(documents_with_previous_term) > 0 and len(documents_with_next_term) > 0): # και οι δύο όροι κλειδιά (terms) υπάρχουν στο ευρετήριο
                matching_papers = set(documents_with_previous_term) & set(documents_with_next_term)
            
        elif term == "or" and i > 0 and i < len(terms) - 1:                  # Έλεγχος για το αν ο όρος κλειδί (term) είναι "or" και αν βρίσκεται μεταξύ δύο όρων κλειδιών (terms)
            previous_term = terms[i - 1]                                     # Αρχικοποίηση του προηγούμενου όρου κλειδιού (previous_term) από τον όρο κλειδί (term) που εξετάζουμε
            next_term = terms[i + 1]                                         # Αρχικοποίηση του επόμενου όρου κλειδιού (next_term) από τον όρο κλειδί (term) που εξετάζουμε
            if previous_term in inverted_index:
                documents_with_previous_term = inverted_index[previous_term] # Ανάκτηση των αριθμών των εργασιών που περιέχουν τον προηγούμενο όρο κλειδί (previous_term)
                for document in documents_with_previous_term:                # Προσπέλαση των αριθμών των εργασιών που περιέχουν τον προηγούμενο όρο κλειδί (previous_term)
                    matching_papers.append(document)                         # Προσθήκη του αριθμού της εργασίας στη λίστα με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης
            if next_term in inverted_index:
                documents_with_next_term = inverted_index[next_term]         # Ανάκτηση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                for document in documents_with_next_term:                    # Προσπέλαση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                    matching_papers.append(document)                         # Προσθήκη του αριθμού της εργασίας στη λίστα με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης

        elif term == "not" and i < len(terms) - 1:                           # Έλεγχος για το αν ο όρος κλειδί (term) είναι "not" και αν βρίσκεται πριν τον τελευταίο όρο κλειδί (terms)
            next_term = terms[i + 1]                                         # Αρχικοποίηση του επόμενου όρου κλειδιού (next_term) από τον όρο κλειδί (term) που εξετάζουμε
            if next_term in inverted_index:
                documents_with_next_term = inverted_index[next_term]         # Ανάκτηση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term)
                all_papers = set(range(num_of_papers))                       # Αρχικοποίηση της λίστας με όλους τους αριθμούς των εργασιών και μετατροπή της σε σύνολο
                non_matching_papers = all_papers - set(documents_with_next_term) # Αφαίρεση των αριθμών των εργασιών που περιέχουν τον επόμενο όρο κλειδί (next_term) από τη λίστα με όλους τους αριθμούς των εργασιών και μετατροπή της σε σύνολο
                for document in non_matching_papers:           
                    matching_papers.append(document)                         # Προσθήκη του αριθμού της εργασίας στη λίστα με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης

    
    overall_matching_papers = set(matching_papers)
    return overall_matching_papers                     # Αφαίρεση των διπλότυπων αριθμών εργασιών που περιέχουν το ερώτημα αναζήτησης


def search_papers_vector_space(query, papers, preprocessed_papers):

    # Step 1: Tokenize and preprocess the text
    tokenized_query = nltk.word_tokenize(preprocess_text(query))                         # Μετατροπή του ερωτήματος αναζήτησης σε λεκτικές μονάδες και προεπεξεργασία του κειμένου
    doc_id = [doc['id'] for doc in papers]                                               # Λίστα με τους αριθμούς των εργασιών
    #title = [doc['title'] for doc in papers]
    preprocessed_abstracts = [doc['abstract'] for doc in preprocessed_papers]            # Λίστα με τις προεπεξεργασμένες περιλήψεις (abstracts) των εργασιών
    tokenized_abstracts = [nltk.word_tokenize(doc) for doc in preprocessed_abstracts]    # Λίστα με τις λεκτικές μονάδες των προεπεξεργασμένων περιλήψεων (abstracts) των εργασιών

    # Step 2: Calculate TF-IDF
    # Convert tokenized documents to text
    preprocessed_abstracts = [' '.join(doc) for doc in tokenized_abstracts]              # Μετατροπή των λεκτικών μονάδων των περιλήψεων (abstracts) σε κείμενο
    preprocessed_query = ' '.join(tokenized_query)                                       # Μετατροπή των λεκτικών μονάδων του ερωτήματος αναζήτησης σε κείμενο

    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()                                                 # Δημιουργία ενός TF-IDF vectorizer
    tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_abstracts)                # Μετατροπή των προεπεξεργασμένων περιλήψεων (abstracts) σε TF-IDF vectors

    # Transform the query into a TF-IDF vector
    query_vector = tfidf_vectorizer.transform([preprocessed_query])                      # Μετατροπή του ερωτήματος αναζήτησης σε TF-IDF vector

    # Step 3: Calculate cosine similarity
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix)                  # Υπολογισμός της συνημιτονικής ομοιότητας του ερωτήματος αναζήτησης με τα TF-IDF vectors των περιλήψεων (abstracts) των εργασιών

    # Step 4: Rank documents by similarity
    results = [(doc_id[i], cosine_similarities[0][i]) for i in range(len(doc_id))]       # Αποθήκευση των αριθμών των εργασιών και των συνημιτονικών ομοιοτήτων τους σε μία λίστα
    results.sort(key=lambda x: x[1], reverse=True)                                       # Ταξινόμηση του αποτελέσματος

    # Print the ranked documents
    for doc, similarity in results:                                                      # Εκτύπωση των αριθμών των εργασιών και των συνημιτονικών ομοιοτήτων τους
        print(f"Similarity: {similarity:.4f}\n{doc}\n")
    
    return set()


def search_papers_okapi_bm25(query, papers, preprocessed_papers):

    tokenized_query = nltk.word_tokenize(preprocess_text(query))
    doc_id = [doc['id'] for doc in papers]
    preprocessed_abstracts = [doc['abstract'] for doc in preprocessed_papers]
    tokenized_abstracts = [nltk.word_tokenize(doc) for doc in preprocessed_abstracts]

    return set()


def search_papers_default(query, inverted_index):

    terms = query.lower().split()                # Μετατροπή του ερωτήματος αναζήτησης σε πεζά και διαχωρισμός του σε λεκτικές μονάδες
    matching_papers = []                         # Αρχικοποίηση της λίστας με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης

    for term in terms:                           # Προσπέλαση των λεκτικών μονάδων του ερωτήματος αναζήτησης
        if term in inverted_index:               # Ο όρος κλειδί (term) υπάρχει στο ευρετήριο
            documents = inverted_index[term]     # Ανάκτηση των αριθμών των εργασιών που περιέχουν τον όρο κλειδί (term)
            for document in documents:           # Προσπέλαση των αριθμών των εργασιών που περιέχουν τον όρο κλειδί (term)
                matching_papers.append(document) # Προσθήκη του αριθμού της εργασίας στη λίστα με τους αριθμούς των εργασιών που περιέχουν το ερώτημα αναζήτησης

    
    return set(matching_papers)                  # Αφαίρεση των διπλότυπων αριθμών εργασιών που περιέχουν το ερώτημα αναζήτησης