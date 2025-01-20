import numpy as np
from collections import Counter
import math

# Συνάρτηση υπολογισμού TF-IDF για το σύνολο δεδομένων
def calculate_tfidf(dataset, inverted_index):
    """
    Υπολογισμός TF-IDF για το σύνολο δεδομένων.

    :param dataset: Το σύνολο δεδομένων (λίστα εγγράφων)
    :param inverted_index: Ο αντεστραμμένος πίνακας ευρετηρίου
    :return: Λεξικό με τα TF-IDF scores για κάθε όρο και έγγραφο
    """
    tfidf = {}
    N = len(dataset)
    for term, doc_ids in inverted_index.items():
        df = len(set(doc_ids))
        idf = math.log((N + 1) / (df + 1)) + 1  # Προσαρμοσμένος IDF
        tfidf[term] = {}
        for doc_id in set(doc_ids):
            tf = dataset[doc_id]['content'].split().count(term)
            tfidf[term][doc_id] = tf * idf
    return tfidf

# Συνάρτηση υπολογισμού διανύσματος ερωτήματος
def calculate_query_vector(query, tfidf):
    """
    Υπολογισμός του διανύσματος του ερωτήματος με βάση το TF-IDF.

    :param query: Το ερώτημα του χρήστη (string)
    :param tfidf: Το λεξικό TF-IDF
    :return: Διάνυσμα ερωτήματος (numpy array)
    """
    query_terms = query.split()
    vector = np.zeros(len(tfidf))

    for i, term in enumerate(tfidf):
        if term in query_terms:
            vector[i] = 1  # Εναλλακτικά, μπορεί να υπολογιστεί tf-idf του όρου για μεγαλύτερη ακρίβεια

    return vector

# Συνάρτηση υπολογισμού διανυσμάτων VSM για όλα τα έγγραφα
def calculate_vsm(dataset, inverted_index, tfidf):
    """
    Υπολογισμός των διανυσμάτων VSM για όλα τα έγγραφα.

    :param dataset: Το σύνολο δεδομένων
    :param inverted_index: Ο αντεστραμμένος πίνακας ευρετηρίου
    :param tfidf: Το λεξικό TF-IDF
    :return: Λεξικό με τα διανύσματα εγγράφων
    """
    doc_vectors = {}
    for doc_id in range(len(dataset)):
        vector = np.zeros(len(tfidf))
        for i, term in enumerate(tfidf):
            if doc_id in tfidf[term]:
                vector[i] = tfidf[term][doc_id]
        doc_vectors[doc_id] = vector
    return doc_vectors

# Συνάρτηση κατάταξης εγγράφων με βάση το Vector Space Model
def rank_vsm(query, doc_vectors, tfidf):
    """
    Υπολογισμός κατάταξης εγγράφων με βάση το Vector Space Model.

    :param query: Το ερώτημα του χρήστη
    :param doc_vectors: Τα διανύσματα εγγράφων
    :param tfidf: Το λεξικό TF-IDF
    :return: Λίστα κατάταξης εγγράφων
    """
    query_vector = calculate_query_vector(query, tfidf)
    ranked_docs = []

    for doc_id, doc_vector in doc_vectors.items():
        dot_product = np.dot(query_vector, doc_vector)
        doc_length = np.linalg.norm(doc_vector)
        query_length = np.linalg.norm(query_vector)

        score = dot_product / (doc_length * query_length) if doc_length and query_length else 0
        ranked_docs.append({'doc_id': doc_id, 'score': score})

    return sorted(ranked_docs, key=lambda x: x['score'], reverse=True)

# Συνάρτηση κατάταξης εγγράφων με χρήση απλού TF-IDF
def rank_documents(query, tfidf, dataset):
    """
    Κατάταξη εγγράφων με χρήση απλού TF-IDF score.

    :param query: Το ερώτημα του χρήστη
    :param tfidf: Το λεξικό TF-IDF
    :param dataset: Το σύνολο δεδομένων
    :return: Λίστα κατάταξης εγγράφων
    """
    query_terms = query.split()
    scores = Counter()

    for term in query_terms:
        if term in tfidf:
            for doc_id, score in tfidf[term].items():
                scores[doc_id] += score

    ranked_docs = [{"doc_id": doc_id, "score": score, "title": dataset[doc_id]['title']} for doc_id, score in scores.items()]
    return sorted(ranked_docs, key=lambda x: x['score'], reverse=True)

# Συνάρτηση υπολογισμού BM25
def calculate_bm25(dataset, inverted_index, k1=1.5, b=0.75):
    """
    Υπολογισμός BM25 για τα έγγραφα του dataset.

    :param dataset: Το σύνολο δεδομένων
    :param inverted_index: Ο αντεστραμμένος πίνακας ευρετηρίου
    :param k1: Υπερπαράμετρος ελέγχου ευαισθησίας της συχνότητας (default: 1.5)
    :param b: Υπερπαράμετρος ελέγχου μήκους εγγράφου (default: 0.75)
    :return: Λεξικό BM25 για κάθε όρο και έγγραφο
    """
    N = len(dataset)
    avg_doc_length = sum(len(doc['content'].split()) for doc in dataset) / N
    bm25 = {}

    for term, doc_ids in inverted_index.items():
        df = len(doc_ids)
        idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
        bm25[term] = {}

        for doc_id in set(doc_ids):
            doc_length = len(dataset[doc_id]['content'].split())
            tf = dataset[doc_id]['content'].split().count(term)
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * (doc_length / avg_doc_length))
            bm25[term][doc_id] = idf * (numerator / denominator)

    return bm25

# Συνάρτηση κατάταξης εγγράφων με βάση το BM25
def rank_bm25(query, bm25):
    """
    Κατάταξη εγγράφων με βάση το BM25.

    :param query: Το ερώτημα του χρήστη
    :param bm25: Το λεξικό BM25
    :return: Λίστα κατάταξης εγγράφων
    """
    query_terms = query.split()
    scores = Counter()

    for term in query_terms:
        if term in bm25:
            for doc_id, score in bm25[term].items():
                scores[doc_id] += score

    ranked_docs = [{"doc_id": doc_id, "score": score} for doc_id, score in scores.items()]
    return sorted(ranked_docs, key=lambda x: x['score'], reverse=True)
