import sqlite3
import pandas as pd
import os.path as osp


"""
search specific book in sqlite3 Books.db
"""
def search_database(searchData, dbname: str) -> list[dict]:
    print(type(searchData))
    searchData = searchData.replace(",","")
    searchStr = "%"
    for i in searchData:
        searchStr = searchStr + i + "%"
    conn = sqlite3.connect(osp.join(osp.dirname(__file__), "data", "Books.db"))
    cur = conn.cursor()
    cur.execute(f"""
                SELECT id, title, author, publisher, genres, rating, pages 
                FROM {dbname} 
                WHERE 
                title LIKE \"{searchStr}\" 
                OR 
                author LIKE \"{searchStr}\"
                """)
    data = cur.fetchall()
    print(type(data))
    print(len(data))
    if len(data) != 0:
        searchResult = []
        for i, (id, title, author, publisher, genres, rating, pages) in enumerate(data):
            if dbname == "Korean_book":
                searchResult.append({
                    "key": i,
                    "id": id,
                    "title":title,
                    "author":author,
                    "publisher":publisher,
                    "genres":genres[5:],
                    "rating":rating,
                    "pages":pages
                })
            else:
                searchResult.append({
                    "key": i,
                    "id": id,
                    "title":title,
                    "author":author,
                    "publisher":publisher,
                    "genres":genres,
                    "rating":rating,
                    "pages":pages
                })
        cur.close()
        conn.close()
        return searchResult
    else:
        cur.close()
        conn.close()
        return []



"""
create foreign_book table and insert all foregin_book data
"""
def insert_foreign_books():
    conn = sqlite3.connect("./data/Books.db")
    cur = conn.cursor()
    conn.execute("""
            CREATE TABLE Foreign_book(
                id INTEGER,
                title TEXT,
                genres TEXT,
                author TEXT,
                rating REAL, 
                publisher TEXT, 
                p_date INTEGER, 
                pages INTEGER, 
                language TEXT,
                description TEXT, 
                imgUrl TEXT
            )
    """)

    data = pd.read_csv("./data/foreign-books.csv")
    for i in range(len(data)):
        title = data["title"].iloc[i]
        genre_list = data["genres"].iloc[i].replace("[","").replace("]","").replace("\'","")
        author = data["author"].iloc[i]
        rating = data["rating"].iloc[i]
        publisher = data["publisher"].iloc[i]
        p_date = data["publishDate"].iloc[i]
        pages = data["pages"].iloc[i]
        language = data["language"].iloc[i]
        description = data["description"][i]
        imgUrl = data["coverImg"][i]
        cur.execute(
            'INSERT INTO Foreign_book VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (i, title, genre_list, author, rating, publisher, p_date, pages, language, description, imgUrl)
        )
        print(i, title)
        conn.commit()

    conn.close()