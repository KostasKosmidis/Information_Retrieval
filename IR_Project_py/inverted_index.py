# Εισαγωγή των απαιτούμενων βιβλιοθηκών
import json
from collections import defaultdict

# ------ Δημιουργία Αντεστραμμένου Ευρετηρίου ------
def create_inverted_index(dataset):
    """
    Δημιουργεί το αντεστραμμένο ευρετήριο από το σύνολο των εγγράφων.
    :param dataset: Λίστα με τα έγγραφα, όπου κάθε έγγραφο είναι λεξικό με κλειδί 'content'.
    :return: Το αντεστραμμένο ευρετήριο, το οποίο αντιστοιχεί κάθε λέξη σε μια λίστα από έγγραφα (IDs).
    """
    inverted_index = defaultdict(set)  # Χρησιμοποιούμε set για αποφυγή επαναλήψεων

    # Επεξεργασία κάθε εγγράφου στο dataset
    for doc_id, doc in enumerate(dataset):
        # Διαχωρισμός του περιεχομένου του εγγράφου σε λέξεις
        for word in doc['content'].split():
            inverted_index[word].add(doc_id)  # Προσθήκη του document ID στο set της λέξης

    # Μετατροπή των set σε λίστες και επιστροφή του ευρετηρίου
    return {key: list(value) for key, value in inverted_index.items()}

# ------ Αποθήκευση Αντεστραμμένου Ευρετηρίου σε Αρχείο ------
def save_inverted_index(index, file_path='inverted_index.json'):
    """
    Αποθηκεύει το αντεστραμμένο ευρετήριο σε αρχείο JSON.
    :param index: Το αντεστραμμένο ευρετήριο που δημιουργήθηκε.
    :param file_path: Η διαδρομή αποθήκευσης του αρχείου (προεπιλογή: 'inverted_index.json').
    """
    # Αποθήκευση του ευρετηρίου σε αρχείο JSON
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=4)
    print(f"Ευρετήριο αποθηκεύτηκε στο {file_path}")