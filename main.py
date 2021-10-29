import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.metrics.pairwise import cosine_similarity

books = pd.read_csv("data/Books.csv", low_memory=False)
users = pd.read_csv("data/Users.csv", low_memory=False)
ratings = pd.read_csv("data/Ratings.csv", low_memory=False)

books = books[~books["Year-Of-Publication"].isin(['DK Publishing Inc', 'Gallimard'])]
books["Year-Of-Publication"] = pd.to_numeric(books["Year-Of-Publication"])
users = users[users["Age"] <= 110]
books = books[(books["Year-Of-Publication"] > 1950) & (books["Year-Of-Publication"] <= 2016)]

book_rate = pd.merge(ratings, books, on="ISBN")
book_rate["num_of_rate"] = book_rate.groupby("ISBN").transform("count")["User-ID"]
print(book_rate.head())
top_samples = book_rate.drop_duplicates("ISBN").sort_values("num_of_rate", ascending=False).iloc[:100]["ISBN"]

book_rate = book_rate[book_rate["ISBN"].isin(top_samples)].reset_index(drop=True)

book_rate_pivot = book_rate.pivot(index="User-ID", columns="ISBN", values="Book-Rating")
print(book_rate_pivot.head())
print(book_rate.isnull().sum())

sample_for_users = book_rate_pivot[~book_rate_pivot.isna()].count(axis=1).reset_index()
print(sample_for_users[sample_for_users[0] > 50])

book_rate_clean = book_rate_pivot.fillna(book_rate_pivot.mean(axis=0))

book_matrix = cosine_similarity(book_rate_clean.values)

user_sample = book_rate[
    (book_rate["Book-Title"] == "Life of Pi") & (book_rate["Book-Rating"] == 10) & (book_rate["num_of_rate"] >= 50)]

print(user_sample)
users_to_copy = np.array(user_sample["User-ID"]) #### fix out the list, we need to have axis = 0
print(users_to_copy)


def bookFilter(user_ID):
    index = user_ID
    scores = list(enumerate(book_matrix[index]))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:101]
    unrated = book_rate_pivot.iloc[index][book_rate_pivot.iloc[index].isna()].index
    rated = (book_rate_pivot[unrated].T * book_matrix[index]).T
    rated = rated.iloc[[x[0] for x in scores]].mean()
    rated = rated.reset_index().dropna().sort_values(0, ascending=False).iloc[:10]
    recommended_books = book_rate[book_rate['ISBN'].isin(rated['ISBN'])][['ISBN', 'Book-Title']]
    recommended_books = recommended_books.drop_duplicates('ISBN').reset_index(drop=True)
    assumed_ratings = rated[0].reset_index(drop=True)
    print(pd.DataFrame({'ISBN': recommended_books['ISBN'],
                        'Recommended Book': recommended_books['Book-Title'],
                        'Assumed Rating': assumed_ratings}))
    return pd.DataFrame({'ISBN': recommended_books['ISBN'],
                         'Recommended Book': recommended_books['Book-Title'],
                         'Assumed Rating': assumed_ratings})


for user in users_to_copy:
    bookFilter(users_to_copy[user])
