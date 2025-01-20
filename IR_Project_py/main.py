import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer("english")

from web_crawler import save_dataset
from web_crawler import crawl_articles
from text_preprocessing import preprocess_dataset
from inverted_index import create_inverted_index
from inverted_index import save_inverted_index
from ranking import calculate_tfidf, rank_documents, calculate_vsm, rank_vsm, calculate_bm25, rank_bm25
from evaluation import evaluate_retrieval, calculate_map

def main():
    dataset = crawl_articles()
    save_dataset(dataset, 'dataset.json')
    dataset = preprocess_dataset(dataset)
    inverted_index = create_inverted_index(dataset)
    save_inverted_index(inverted_index, file_path='inverted_index.json')

    while True:
        print("\nΕισάγετε τη λέξη κλειδί σας ή γράψτε 'exit' για τερματισμό:")
        query = input("Κλειδί: ").lower()

        if query == 'exit':
            print("Τερματισμός προγράμματος.")
            break

        print("\nΕπιλέξτε αλγόριθμο:")
        print("1. TF-IDF")
        print("2. Vector Space Model (VSM)")
        print("3. Okapi BM25")
        print("Γράψτε 'exit' για τερματισμό.")
        algorithm_choice = input("Επιλογή (1, 2, 3): ").strip()

        if algorithm_choice.lower() == 'exit':
            print("Τερματισμός προγράμματος.")
            break

        relevant_docs = [[0, 2]]  # Μόνο ένα ερώτημα
        retrieved_docs = []  # Λίστα για αποθήκευση των επιστρεφόμενων εγγράφων

        if algorithm_choice == "1":
            print("\nΧρησιμοποιώντας αλγόριθμο TF-IDF...")
            tfidf = calculate_tfidf(dataset, inverted_index)
            ranked_docs = rank_documents(query, tfidf, dataset)
        elif algorithm_choice == "2":
            print("\nΧρησιμοποιώντας Vector Space Model (VSM)...")
            tfidf = calculate_tfidf(dataset, inverted_index)
            doc_vectors = calculate_vsm(dataset, inverted_index, tfidf)
            ranked_docs = rank_vsm(query, doc_vectors, tfidf)
        elif algorithm_choice == "3":
            print("\nΧρησιμοποιώντας Okapi BM25...")
            bm25_scores = calculate_bm25(dataset, inverted_index)
            ranked_docs = rank_bm25(query, bm25_scores)
        else:
            print("Μη έγκυρη επιλογή αλγορίθμου. Δοκιμάστε ξανά.")
            continue

        print("\nΑποτελέσματα αναζήτησης:")
        if not ranked_docs:
            print("Δεν βρέθηκαν αποτελέσματα.")
        for doc in ranked_docs:
            try:
                doc_id = int(doc.get('doc_id'))
                title = dataset[doc_id].get('title', 'Άγνωστος τίτλος')
                retrieved_docs.append(doc_id)
                print(f"{title} (Βαθμολογία: {doc['score']:.4f})")
            except (ValueError, KeyError) as e:
                print(f"Σφάλμα με το doc_id: {doc.get('doc_id')} - {e}")

        # Εισαγωγή στο σύστημα αξιολόγησης
        evaluation_metrics = evaluate_retrieval(relevant_docs[0], retrieved_docs)
        print("\nΑξιολόγηση Αποτελεσμάτων:")
        print(f"Precision: {evaluation_metrics['precision']:.4f}")
        print(f"Recall: {evaluation_metrics['recall']:.4f}")
        print(f"F1 Score: {evaluation_metrics['f1_score']:.4f}")

        # Υπολογισμός MAP
        map_score = calculate_map(relevant_docs, [retrieved_docs])
        print(f"\nMean Average Precision (MAP): {map_score:.4f}")

if __name__ == "__main__":
    main()

