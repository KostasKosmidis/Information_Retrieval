# Εισαγωγή της βιβλιοθήκης για την προετοιμασία του κειμένου
from text_preprocessing import preprocess_text

# ------ Επεξεργασία Boolean Ερωτήματος ------
def query_processing(terms, num_of_docs):
    """
    Επεξεργάζεται Boolean ερωτήματα και επιστρέφει τα αποτελέσματα.
    :param terms: Λίστα όρων και τελεστών του ερωτήματος.
    :param num_of_docs: Συνολικός αριθμός εγγράφων στη συλλογή.
    :return: Λίστα εγγράφων που πληρούν το ερώτημα.
    """
    results_stack = []  # Στοίβα για να αποθηκεύουμε τα αποτελέσματα
    all_docs = set(range(num_of_docs))  # Σύνολο όλων των εγγράφων

    for i, term in enumerate(terms):  # Για κάθε όρο του ερωτήματος
        if isinstance(term, list):  # Αν ο όρος είναι λίστα (έγγραφα)
            results_stack.append(set(term))  # Προσθέτουμε τα έγγραφα στη στοίβα
        elif term == "and":  # Αν ο όρος είναι 'and'
            if len(results_stack) >= 2:  # Αν υπάρχουν τουλάχιστον δύο όροι
                set2 = results_stack.pop()  # Παίρνουμε το δεύτερο σύνολο
                set1 = results_stack.pop()  # Παίρνουμε το πρώτο σύνολο
                results_stack.append(set1 & set2)  # Επιστρέφουμε την τομή των δύο συνόλων
            else:
                raise ValueError("Λάθος σύνταξη ερωτήματος: Λείπουν όροι για 'and'.")
        elif term == "or":  # Αν ο όρος είναι 'or'
            if len(results_stack) >= 2:  # Αν υπάρχουν τουλάχιστον δύο όροι
                set2 = results_stack.pop()  # Παίρνουμε το δεύτερο σύνολο
                set1 = results_stack.pop()  # Παίρνουμε το πρώτο σύνολο
                results_stack.append(set1 | set2)  # Επιστρέφουμε την ένωση των δύο συνόλων
            else:
                raise ValueError("Λάθος σύνταξη ερωτήματος: Λείπουν όροι για 'or'.")
        elif term == "not":  # Αν ο όρος είναι 'not'
            if results_stack:  # Αν υπάρχουν όροι στη στοίβα
                set1 = results_stack.pop()  # Παίρνουμε το πρώτο σύνολο
                results_stack.append(all_docs - set1)  # Επιστρέφουμε την διαφορά όλων των εγγράφων με το set1
            else:
                raise ValueError("Λάθος σύνταξη ερωτήματος: Λείπει όρος για 'not'.")

    if len(results_stack) != 1:  # Αν το αποτέλεσμα δεν είναι μοναδικό
        raise ValueError("Λάθος σύνταξη ερωτήματος: Το αποτέλεσμα δεν είναι μοναδικό.")
    
    return sorted(results_stack.pop())  # Επιστρέφουμε το τελικό αποτέλεσμα, ταξινομημένο


# ------ Αντικατάσταση Όρων με Έγγραφα από το Ευρετήριο ------
def replace_terms_with_docs(query, inverted_index):
    """
    Αντικαθιστά τους όρους του ερωτήματος με τα έγγραφα που τους περιέχουν.
    :param query: Το αρχικό ερώτημα χρήστη.
    :param inverted_index: Το αντεστραμμένο ευρετήριο.
    :return: Λίστα όρων, τελεστών και εγγράφων.
    """
    terms = preprocess_text('boolean query', query).split()  # Προετοιμασία του κειμένου
    processed_terms = []  # Λίστα για αποθήκευση των επεξεργασμένων όρων

    for term in terms:  # Για κάθε όρο του ερωτήματος
        if term in {"and", "or", "not", "(", ")"}:  # Αν ο όρος είναι τελεστής ή παρένθεση
            processed_terms.append(term)  # Προσθέτουμε τον τελεστή στη λίστα
        else:
            if term in inverted_index:  # Αν ο όρος υπάρχει στο ευρετήριο
                processed_terms.append(inverted_index[term])  # Αντικαθιστούμε τον όρο με τα έγγραφα του
            else:
                raise ValueError(f"Ο όρος '{term}' δεν βρέθηκε στο ευρετήριο.")  # Σφάλμα αν δεν βρεθεί ο όρος
    
    return processed_terms  # Επιστρέφουμε τη λίστα με τους επεξεργασμένους όρους