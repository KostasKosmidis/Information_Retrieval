# ------ Αξιολόγηση Ανάκτησης Εγγράφων ------
def evaluate_retrieval(relevant_docs, retrieved_docs):
    """
    Υπολογίζει τις βασικές μετρικές αξιολόγησης για την ανάκτηση εγγράφων.
    :param relevant_docs: Λίστα με τα σχετικά έγγραφα για το ερώτημα.
    :param retrieved_docs: Λίστα με τα ανακτηθέντα έγγραφα από το σύστημα.
    :return: Λεξικό με precision, recall και f1_score.
    """
    relevant_set = set(relevant_docs)  # Σύνολο των σχετικών εγγράφων
    retrieved_set = set(retrieved_docs)  # Σύνολο των ανακτηθέντων εγγράφων

    # Υπολογισμός των True Positives (έγγραφα που είναι και σχετικά και ανακτηθέντα)
    true_positives = len(relevant_set & retrieved_set)
    
    # Υπολογισμός της ακρίβειας (Precision)
    precision = true_positives / len(retrieved_set) if retrieved_set else 0
    
    # Υπολογισμός της ανακλητικότητας (Recall)
    recall = true_positives / len(relevant_set) if relevant_set else 0
    
    # Υπολογισμός του F1 score
    f1_score = (2 * precision * recall) / (precision + recall) if precision + recall > 0 else 0

    # Επιστροφή των αποτελεσμάτων σε μορφή λεξικού
    return {"precision": precision, "recall": recall, "f1_score": f1_score}

# ------ Υπολογισμός Μέσης Μέσης Ακρίβειας (MAP) ------
def calculate_map(relevant_docs, retrieved_docs):
    """
    Υπολογισμός Mean Average Precision (MAP) για πολλαπλά ερωτήματα.
    :param relevant_docs: Λίστα λιστών με τα σχετικά έγγραφα για κάθε ερώτημα.
    :param retrieved_docs: Λίστα λιστών με τα ανακτηθέντα έγγραφα για κάθε ερώτημα.
    :return: Η μέση ακρίβεια (MAP).
    """
    # Έλεγχος συμβατότητας των λιστών
    if len(relevant_docs) != len(retrieved_docs):
        print(f"Ασυμβατότητα λιστών: relevant_docs={len(relevant_docs)}, retrieved_docs={len(retrieved_docs)}")
        return 0

    ap_sum = 0  # Άθροισμα των μέσων ακρίβειας για όλα τα ερωτήματα
    for query_id, relevant_set in enumerate(relevant_docs):  # Για κάθε ερώτημα
        retrieved_set = retrieved_docs[query_id]  # Ανάκτηση των ανακτηθέντων εγγράφων
        precision_values = []  # Λίστα για την αποθήκευση των τιμών ακρίβειας
        relevant_found = 0  # Μετρητής για τα σχετικά έγγραφα που βρέθηκαν

        # Υπολογισμός της ακρίβειας για κάθε ανακτηθέν έγγραφο
        for i, doc_id in enumerate(retrieved_set):
            if doc_id in relevant_set:  # Αν το έγγραφο είναι σχετικό
                relevant_found += 1
                precision_values.append(relevant_found / (i + 1))  # Υπολογισμός ακρίβειας

        # Υπολογισμός της μέσης ακρίβειας (AP) για το ερώτημα
        if precision_values:
            ap_sum += sum(precision_values) / len(relevant_set)

    # Υπολογισμός του MAP (Μέση Μέση Ακρίβεια) για όλα τα ερωτήματα
    return ap_sum / len(relevant_docs) if relevant_docs else 0
