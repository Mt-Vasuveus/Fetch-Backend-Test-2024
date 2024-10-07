from flask import Flask, jsonify, g
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

########################
# Initialize Database
########################
DATABASE = "points.db"

# Returns the database if it doesn't exist yet
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        try:
            db = g._database = sqlite3.connect(DATABASE)
        except:
            print("Error with Database")
            quit()

    return db

# Create necessary structure in database
def init_db():
    with app.app_context():
        init_query = "CREATE TABLE IF NOT EXISTS points(payer TEXT, points INTEGER, timestamp TEXT)"
        query_db(init_query)
    return

# From Flask Documentation https://flask.palletsprojects.com/en/3.0.x/patterns/sqlite3/
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    results = cur.fetchall()
    cur.close()
    return (results[0] if results else None) if one else results

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_database", None)
    if db is None:
        db.close()



########################
# API Calls
########################
@app.route("/add", methods=['POST'])
def add_point():
    print("adding points")

@app.route("/spend", methods=['POST'])
def spend_points():
    print("spending points")

@app.route("/balance", methods=['GET'])
def get_balance():
    print("getting points")


########################
# Start Server
########################
if __name__ == "__main__":
    init_db()
    app.run(port = 8000)