import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

df_all = pd.read_csv("data/Books.csv")
### some summary statistics before start
#print(df_all.head())
#print(df_all.shape)
#print(df_all.info())
df = df_all.iloc[:100000, :]
#print(df.shape)
#print(df.describe())
#print(df.isnull().sum())
#print(len(df["Book-Title"].unique()))
#print(len(df["Book-Author"].unique()))
#print(len(df["Publisher"].unique()))
book_users_all = pd.read_csv("data/Users.csv")
book_rating_all = pd.read_csv("data/Ratings.csv")
book_rating = book_rating_all.iloc[:100000, :]
book_users = book_users_all.iloc[:100000, :]
#print(book_users.isnull().sum())
#print(book_rating.head())
book_ratings = book_rating.iloc[:, 0:3]
#print(book_ratings)
#print(df.head(2))

book_ratings.rename(columns={"User-ID" : "user_id", "Book-Rating" : "book_rating"}, inplace=True)
#print(df)
df = pd.merge(df, book_ratings, on="ISBN")
#print(df.head())
df = df.reindex(columns=["ISBN", "user_id", "Book-Title", "Book-Author", "Year-Of-Publication", "Publisher", "book_rating", "Image-URL-S", "Image-URL-M", "Image-URL-L"])
#print(df)
a = df.groupby("Book-Title").mean()["book_rating"].sort_values(ascending=False)
b = df.groupby("Book-Title").count()["book_rating"].sort_values(ascending=False)
#print(a, b)
ratings = pd.DataFrame(df.groupby("Book-Title").mean()["book_rating"])
#print(ratings.tail())
ratings["num_of_ratings"] = pd.DataFrame(df.groupby("Book-Title").count()["book_rating"])
#print(ratings.tail())
#print(ratings.sort_values(by="book_rating", ascending=False))


matrix_book = df.pivot_table(index="user_id", columns="Book-Title", values="book_rating")
#print(book_metrix)
print(ratings.sort_values("num_of_ratings", ascending=False))
davinci_code_ratings = matrix_book["The Da Vinci Code"]
#print(davinci_code_ratings.head())
similar_davinci = matrix_book.corrwith(davinci_code_ratings)
#print(similar_davinci)
corr_dav = pd.DataFrame(similar_davinci, columns=["Correlation"])
#print(corr_dav.head())
corr_dav.isnull().sum()
corr_dav.dropna(inplace=True)
corr_dav.isnull().sum()
#print(corr_dav.head())
corr_dav = corr_dav.join(ratings["num_of_ratings"])
#print(corr_dav.head())
corr_dav[corr_dav.num_of_ratings > 50].sort_values("Correlation", ascending=False)


def predictBooks():
    book_name = input("Write some of the books you read, from out DataSet: ")
    book_user_ratings = matrix_book[book_name]
    similar_to_book_name = matrix_book.corrwith(book_user_ratings)

    corr_book_name = pd.DataFrame(similar_to_book_name, columns=["Correlation"])
    corr_book_name.dropna(inplace=True)

    corr_user_book = corr_book_name.join(ratings["num_of_ratings"])
    predictions = corr_user_book[corr_user_book.num_of_ratings > 50].sort_values("Correlation", ascending=False)
    print(predictions)
    return predictions

predictBooks()


