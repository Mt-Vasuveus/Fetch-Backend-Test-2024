from flask import Flask, jsonify
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

@app.route("/add", methods=['POST'])
def addPoint():
    print("adding points")

@app.route("/spend", methods=['POST'])
def spendPoints():
    print("spending points")

@app.route("/balance", methods=['GET'])
def spendPoints():
    print("getting points")

if __name__ == "__main__":
    app.run(port = 8000)