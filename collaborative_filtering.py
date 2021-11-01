# Try this!!!!!
import pandas as pd

books = pd.read_csv("data/Books.csv", low_memory=False)
users = pd.read_csv("data/Users.csv", low_memory=False)
ratings = pd.read_csv("data/Ratings.csv", low_memory=False)
books = books.iloc[:100000, :]
ratings = ratings.iloc[:100000, :]
users = users.iloc[:100000, :]
ratings_book = pd.merge(books, ratings, on="ISBN").drop(["Publisher"], axis=1)

ratings_book["num_of_rate"] = ratings_book.groupby("ISBN").transform("count")["User-ID"]
ratings_book = ratings_book[ratings_book["num_of_rate"] >= 25]

user_rating = ratings_book.pivot_table(index="User-ID", columns="Book-Title", values="Book-Rating")

user_rating = user_rating.dropna(thresh=10, axis=1).fillna(0)

book_similarity_df = user_rating.corr(method="pearson")



def similarity_books(book_title, rate):
    scores = book_similarity_df[book_title] * (rate - 2.5)
    scores = scores.sort_values(ascending=False)
    print(scores)
    return scores



favorite_books = [("Girl with a Pearl Earring", 4),("Life of Pi", 5),("A Map of the World", 3)]
similar_books = pd.DataFrame()
for book, rate in favorite_books:
    similar_books = similar_books.append(similarity_books(book, rate), ignore_index=True)
print(similar_books.head())
print(similar_books.sum().sort_values(ascending=False))




