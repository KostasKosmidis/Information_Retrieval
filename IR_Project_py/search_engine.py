# Εισαγωγή των απαιτούμενων συναρτήσεων
from query_processing import process_query
from ranking import calculate_tfidf, rank_documents

# ------ Μηχανή Αναζήτησης ------
def search_engine(query, dataset, inverted_index):
    """
    Λειτουργία Μηχανής Αναζήτησης που επεξεργάζεται το ερώτημα, υπολογίζει το TF-IDF και κατατάσσει τα έγγραφα.
    :param query: Το ερώτημα αναζήτησης από τον χρήστη.
    :param dataset: Το σύνολο των εγγράφων προς αναζήτηση.
    :param inverted_index: Το αντεστραμμένο ευρετήριο για τα έγγραφα.
    :return: Εκτυπώνει τα αποτελέσματα αναζήτησης.
    """
    print("\n=== Μηχανή Αναζήτησης ===")
    print(f"Ερώτημα: {query}")  # Εκτύπωση του ερωτήματος

    # Επεξεργασία του ερωτήματος και εύρεση των σχετικών εγγράφων
    relevant_docs = process_query(query, inverted_index)
    
    # Αν δεν βρεθούν σχετικά έγγραφα
    if not relevant_docs:
        print("Δεν βρέθηκαν αποτελέσματα.")
        return

    # Υπολογισμός του TF-IDF για όλα τα έγγραφα
    tfidf = calculate_tfidf(dataset, inverted_index)
    
    # Κατάταξη των εγγράφων με βάση τα αποτελέσματα του TF-IDF
    ranked_docs = rank_documents(query, tfidf, dataset)

    # Εκτύπωση των αποτελεσμάτων αναζήτησης
    print("\nΑποτελέσματα αναζήτησης:")
    for doc in ranked_docs:
        print(f"{doc['title']} (Βαθμολογία: {doc['score']:.4f})")
