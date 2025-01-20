# Εισαγωγή απαραίτητων βιβλιοθηκών
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

# Λήψη απαραίτητων πόρων από το NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Συνάρτηση για την προεπεξεργασία ενός κειμένου
def preprocess_text(text):
    """
    Εκτελεί προεπεξεργασία στο δοσμένο κείμενο, αφαιρώντας μη αλφαβητικούς χαρακτήρες,
    διαχωρίζοντας σε λέξεις, μετατρέποντας σε πεζά, αφαιρώντας stopwords, και εφαρμόζοντας stemming.

    :param text: Το εισαγόμενο κείμενο (string)
    :return: Επεξεργασμένο κείμενο (string)
    """
    # Αφαίρεση μη αλφαβητικών χαρακτήρων
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Διαχωρισμός του κειμένου σε λέξεις και μετατροπή σε πεζά
    tokens = word_tokenize(text.lower())
    
    # Αφαίρεση των stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Εφαρμογή stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    
    return " ".join(tokens)

# Συνάρτηση για την προεπεξεργασία ενός dataset που περιέχει πολλαπλά κείμενα
def preprocess_dataset(dataset):
    """
    Εκτελεί προεπεξεργασία στο περιεχόμενο κάθε εγγράφου του dataset.

    :param dataset: Λίστα από dictionaries με το κλειδί 'content' να περιέχει το κείμενο
    :return: Dataset με επεξεργασμένο περιεχόμενο
    """
    for doc in dataset:
        doc['content'] = preprocess_text(doc['content'])
    return dataset

