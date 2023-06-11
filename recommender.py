import pickle

# Importing the necessary modules
import gzip
import pandas as pd

def get_recs(liked_books):
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

    # Loading the pickle file containing CSV mapping dataset
    csv_book_mapping = load_pickle_file("ml/csv_book_mapping.pkl", "CSV Mapping Dataset")

    # Loading the pickle file containing interactions dataset
    goodreads_interactions = load_pickle_file("ml/book_interactions.pkl", "Interactions Dataset")

    # Converting liked book IDs to integer values based on the CSV mapping
    for i in range(len(liked_books)):
        liked_books[i] = int(csv_book_mapping[liked_books[i]])

    # Filtering interactions dataset for recommended users
    rec_users = goodreads_interactions[(goodreads_interactions['rating'] >= 4) & (goodreads_interactions['book_id'].isin(liked_books))]

    # Extracting recommended user IDs
    rec_users = (rec_users["user_id"].values).tolist()

    # Filtering interactions dataset for recommended lines
    rec_lines = (goodreads_interactions[goodreads_interactions['user_id'].isin(rec_users)])

    # Creating a new dictionary to map book IDs back to their original values
    new_book_mapping = {value: key for key, value in csv_book_mapping.items()}

    # Creating a dataframe for recommended lines
    recs = pd.DataFrame(rec_lines, columns=["user_id", "book_id", "rating"])
    recs["book_id"] = recs["book_id"].astype(str)
    recs['book_id'] = recs['book_id'].map(new_book_mapping)
 
    # Counting the top recommended books
    top_recs = recs["book_id"].value_counts().head(10)
    top_recs = top_recs.index.values

    # Reading book titles from a JSON file
    books_titles = pd.read_json("ml/books_titles.json")
    books_titles["book_id"] = books_titles["book_id"].astype(str)

    # Counting all recommended books
    all_recs = recs["book_id"].value_counts()

    # Merging the book count and titles dataframes
    all_recs = all_recs.to_frame().reset_index()
    all_recs.columns = ["book_id", "book_count"]
    all_recs = all_recs.merge(books_titles, how="inner", on="book_id")

    # Calculating the score for each recommended book
    all_recs["score"] = all_recs["book_count"] * (all_recs["book_count"] / all_recs["ratings"])

    # Sorting recommended books by score in descending order and selecting the top 10
    all_recs = all_recs.sort_values("score", ascending=False).head(10)
    
    return all_recs
