import pickle

# Importing the necessary modules
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import gzip

def search(query):
    def load_pickle_file(file_path, variable_name):
        try:
            # Opening the pickle file and loading the object
            with gzip.open(file_path, 'rb') as file:
                p = pickle.Unpickler(file)
                variable = p.load()
            return variable
        except Exception as e:
            # Printing an error message if an exception occurs during loading
            print(f"An error occurred loading {variable_name}:", str(e))
            exit()

    # Loading the necessary pickle files
    titles = load_pickle_file("ml/titles.pkl", "Book Titles Dataset")
    tfidf = load_pickle_file("ml/tfidf.pkl", "TFIDF Matrix")
    vectorizer = load_pickle_file("ml/vectorizer.pkl", "Vectorizer")

    # Processing the input similar to the dataset
    processed = re.sub("a-zA-Z0-9 ]", "", query.lower())

    # Transforming the processed query into a vectorizer
    query_vec = vectorizer.transform([processed])

    # Determining the similarity of the two vectors
    similarity = cosine_similarity(query_vec, tfidf).flatten()

    # Finding the 10 largest similarity values
    indicies = np.argpartition(similarity, -10)[-10:]
    results = titles.iloc[indicies]

    # Sorting the values in descending order based on ratings
    results = results.sort_values("ratings", ascending=False)

    return results.head(10).values