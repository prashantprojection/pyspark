import time
import random
import pickle
import numpy as np
from numpy.linalg import norm
import sqlite3
import hashlib

# FOR_GENRE_NUM = 2855
# KOR_GENRE_NUM = 22


def analyse(data, M):
    DATA_PATH = "/home/ljj0512/private/workspace/data-mining/project/backend"
    con = sqlite3.connect(f"{DATA_PATH}/Books.db")
    cur = con.cursor()

    # print(data["books"][0]["title"])
    # print(type(data["books"][0]["id"]))
    if(data["where"]=="korean"):
        # print(data["books"][0]["genres"].split(","))
        # print(len(data["books"][0]["genres"].split(",")[1]))
        for i, d in enumerate(data["books"]):
            data["books"][i]["genres"] = d["genres"].split(",")
        dbname = "Korean_book"
        genre_dim = 2855

    else:
        # print(data["books"][0]["genres"].split(", "))
        # print(len(data["books"][0]["genres"].split(", ")[1]))
        for i, d in enumerate(data["books"]):
            data["books"][i]["genres"] = d["genres"].split(", ")
        dbname = "Foreign_book"
        genre_dim = 980
    # print(data["books"][0]["author"])
    # print(myHash(data["books"][0]["author"]))
    print(type(data["books"]))
    userProfile = make_userProfile(data["books"], data["genres"], data["where"], DATA_PATH)
    print(type(userProfile)) # list면 books 있음.
    topNum = 50
    if len(data["books"]) == 0:
        #genre만 받았을 경우
        top50Data = linear_search(M, userProfile, topNum, genre_dim)
    else:
        top50Data = my_search(M, userProfile, topNum)
    
    
    for i, id in enumerate(top50Data):
        try:
            # print(i)
            cur.execute(
                f"SELECT title, author, publisher, rating, imgUrl FROM {dbname} WHERE id=={id}"
            )
            temp = cur.fetchall()[0]
            temp = {
                "title":temp[0],
                "author":temp[1],
                "publisher":temp[2],
                "rating":temp[3],
                "imgUrl":temp[4],
            }
            top50Data[i] = temp
        except:
            pass
    cur.close()
    con.close()

    return top50Data



def make_userProfile(books, genres, where, path):
    with open(f"{path}/data/{where}-all-genres-dic.pkl", "rb") as f:
        genres_dic = pickle.load(f)

    if len(books) == 0:
        # 0을 남겨둠
        userProfile = np.zeros((1,len(genres_dic)+1))
        for genre in genres:
            userProfile[0,genres_dic[genre]] = 1.
        return userProfile
    else:
        genreVec = np.zeros((len(genres_dic)))
        for genre in genres:
            genreVec[genres_dic[genre]] = 1.

        idVec = []
        authorVec = []
        for one in books:
            for genre in one["genres"]:
                genreVec[genres_dic[genre]-1] += 1.
            idVec.append(one["id"])
            authorVec.append(myHash(one["author"]))

        return [idVec, genreVec, authorVec]




def cos_similarity(x :np.array, y :np.array):
    return ( (np.dot(x,y))/(norm(x)*norm(y)) )

def linear_search(KorBookMatrix, userProfile, topNum, genre_dim):
    similarity = map(
        lambda bookProfile: \
            (int(bookProfile[0]),cos_similarity(bookProfile[1:genre_dim+1], userProfile[0,1:]))
            ,KorBookMatrix)
    best = sorted(similarity, key=lambda t: -t[1])[:topNum]
    return [t[0] for t in best]
    # return [t for t in best]



def mySimilarity(x :np.array, user :np.array):
    if(any(x[0]==user[0])):
        return 0
    elif(any(x[-1]==user[2])):
        return 1.3*((np.dot(x[1:-1],user[1]))/(norm(x[1:-1])*norm((user[1]>0))))
    else:
        return ( (np.dot(x[1:-1],user[1]))/(norm(x[1:-1])*norm((user[1]>0))) )

def my_search(Matrix, userProfile, topNum):
    similarity = map(
        lambda bookProfile: \
            (int(bookProfile[0]),mySimilarity(bookProfile, userProfile))
            ,Matrix)
    best = sorted(similarity, key=lambda t: -t[1])[:topNum]
    return [t[0] for t in best]
    # return [t for t in best]


def myHash(s):
    if s == None:
        return 0
    else:
        return int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16) % (10 ** 9)