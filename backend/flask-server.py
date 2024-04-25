## https://pythonbasics.org/flask-rest-api/
from flask import Flask, request, jsonify
# import ./.venv\lib\python3.10\site-packages\flask
from flask_cors import CORS
import os.path as osp
import json
import pickle
from utils import search_database
from analysis.analyse import analyse

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

@app.route("/foreign", methods=["GET"])
def sent_foreign_genres():
    return jsonify({"reprGenres":repr_genres})


@app.route("/foreign/search=<searchData>", methods=["GET"])
def sent_foreign_search_result(searchData):
    searchData = searchData.encode("UTF-8").decode("UTF-8")
    searchResult = search_database(searchData, "Foreign_book")
    if(searchResult == []):
        searchResult = "null".encode("UTF-8")
        return searchResult
    else:
        return jsonify(searchResult)


@app.route("/recommend", methods=["POST"])
def sent_rec_result():
    with open(f"{DATA_PATH}/response.json", "w") as f:
        json.dump(request.json, f)
        result = analyse(request.json, ForBookMatrix)
    print(len(result))
    print(type(result))
    return jsonify(result)
    # return request.json


if __name__ == "__main__":
    DATA_PATH = osp.join(osp.dirname(__file__), "data")
    PORT = 8088
    HOST = "0.0.0.0"
    try:
        with open(f"{DATA_PATH}/ForBookMatrix.pkl", "rb") as f:
            ForBookMatrix = pickle.load(f)
    except FileNotFoundError:
        print("#### FileNotFoundError")

    # others_genres = []
    # with open(osp.join(DATA_PATH,"korean-all-genres.txt"), "rb") as f:
    #     others_genres = f.read().decode("UTF-8").split("\n")
    #     others_genres = others_genres[:len(others_genres)-1]

    repr_genres = []
    with open(osp.join(DATA_PATH,"foreign-representative-genres.txt"), "rb") as f:
        repr_genres = f.read().decode("UTF-8").split("\n")
        repr_genres = repr_genres[:len(repr_genres)-1]
    # others_genres = []
    # with open(osp.join(DATA_PATH,"foregin-all-genres.txt"), "rb") as f:
    #     others_genres = f.read().decode("UTF-8").split("\n")
    #     others_genres = others_genres[:len(others_genres)-1]

    app.run(host=HOST, port=PORT)