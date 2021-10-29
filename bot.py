import pandas as pd
import warnings
import sys
import time

# reading data and getting rid of all Na`s or Nan`s values
warnings.filterwarnings("ignore")
df_all = pd.read_csv("data/Books.csv")
df = df_all.iloc[:100000, :]
users_all = pd.read_csv("data/Users.csv")
rating_all = pd.read_csv("data/Ratings.csv")
rating = rating_all.iloc[:100000, :]
users = users_all.iloc[:100000, :]

ratings = rating.iloc[:, 0:3]
# renaming columns in ratings data set
ratings.rename(columns={"User-ID": "user_id", "Book-Rating": "book_rating"}, inplace=True)
# merging books dataset with ratings dataset
df = pd.merge(df, ratings, on="ISBN")
df = df.reindex(
    columns=["ISBN", "user_id", "Book-Title", "Book-Author", "Year-Of-Publication", "Publisher", "book_rating",
             "Image-URL-S", "Image-URL-M", "Image-URL-L"])
a = df.groupby("Book-Title").mean()["book_rating"].sort_values(ascending=False)
b = df.groupby("Book-Title").count()["book_rating"].sort_values(ascending=False)
# new ratings dataset grouped by  Book Title with mean ratings
ratings = pd.DataFrame(df.groupby("Book-Title").mean()["book_rating"])
ratings["num_of_ratings"] = pd.DataFrame(df.groupby("Book-Title").count()["book_rating"])
# Pivot Table for user on book title with ratings as value
matrix_book = df.pivot_table(index="user_id", columns="Book-Title", values="book_rating")
# print titles with max amount of num of ratings. Taking Life of Pi as sample to correlate
# print(ratings.sort_values("num_of_ratings", ascending=False))
life_of_pi_ratings = matrix_book["Life of Pi"]
# findings title same as Life of Pi
same_as_life = matrix_book.corrwith(life_of_pi_ratings)
# make a correlation between titles , that a same as Life of Pi
correlation_of_life = pd.DataFrame(same_as_life, columns=["Correlation"])
# Dropping all Null and Na`s
correlation_of_life.dropna(inplace=True)
# print(correlation_of_life.isnull().sum()) to check
# joining correlation dataset with number of ratings
correlation_of_life = correlation_of_life.join(ratings["num_of_ratings"])
# showing results of correlation, where number of ratings is more than 50
correlation_of_life[correlation_of_life.num_of_ratings > 50].sort_values("Correlation", ascending=False)


# Function to make a Correlation Filter with all of the book titles
def bookFilter():
    book_name = input("Write some of the books you read, from out DataSet: ")
    try:
        user_book_name = str(book_name)
        user_rating = matrix_book[user_book_name]
        similar_name = matrix_book.corrwith(user_rating)

        corr_book = pd.DataFrame(similar_name, columns=["Correlation"])
        corr_book.dropna(inplace=True)

        corr_user_book = corr_book.join(ratings["num_of_ratings"])
        predictions = corr_user_book[corr_user_book.num_of_ratings > 50].sort_values("Correlation", ascending=False)
        print(predictions)
        selection = input("Do you want to make another book recommendation? 1 for Yes, 2 for No")
        try:
            bot_selection_number = int(selection)
            print("you have selected: ", bot_selection_number)
        except ValueError:
            print(" Invalid selection")
            print("Going back to menu")
            bot_information()
        if bot_selection_number == 1:
            bookFilter()
        elif bot_selection_number == 2:
            bot_quit()
        else:
            print("Invaild selection \n")
            bot_information()
        return predictions

    except BaseException:
        print("Ow, looks like we do not have your book in Data Base")
        print("Or you have mistakes in book title")
        print("Check it again please. You should have a string as your input")
        print("Try once again. If you see same mistake, try another book")
        time.sleep(5)
        bot_information()




name = input("Please, write your name: ")


def bot_information():
    print("""
           You are using my new bot for book recommendation
-----------------Have fun!------------------
""")
    bot_menu()
    time.sleep(3)


def bot_quit():
    sys.exit("""Thank you for using my bot!
Hope u enjoyed it 
Bye!""")


def bot_menu():
    print("\nHello, " + name + """\nWelcome to Book Recommendation bot in Python.
----Main Menu---
Press 1 for Information.
Press 2 for Book Recommendation.
Press 3 for Quit.
""")
    menu_selection = input("please select your option: \n")
    try:
        menu_selection_number = int(menu_selection)
        print("you have selected: ", menu_selection_number)
    except ValueError:
        print(" Invalid selection")
        bot_information()

    if menu_selection_number == 1:
        bot_information()
    elif menu_selection_number == 2:
        bookFilter()
    elif menu_selection_number == 3:
        bot_quit()
    else:
        print("Invaild selection \n")
        bot_information()


bot_information()
