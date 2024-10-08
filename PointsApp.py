from flask import Flask, request, jsonify, g
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
        init_query = "CREATE TABLE IF NOT EXISTS pointsdb(payer TEXT, points INTEGER, timestamp TEXT);"
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
    if db is not None:
        db.close()

########################
# API Calls
########################
@app.route("/add", methods=['POST'])
def add_point():
    request_json = request.get_json()

    # Check that the json has the data we need
    if ("payer" not in request_json.keys() or
            "points" not in request_json.keys() or 
            "timestamp" not in request_json.keys()):
        return "Invalid JSON", 400
    
    add_query = "INSERT INTO pointsdb VALUES (?, ?, ?);"
    try:
        query_db(add_query, [
            request_json["payer"], 
            request_json["points"], 
            request_json["timestamp"]])
        g._database.commit()
        return "", 200
    except Error as e:
        return "Error adding points", 500


@app.route("/spend", methods=['POST'])
def spend_points():
    print("spending points")
    return "WIP"

@app.route("/balance", methods=['GET'])
def get_balance():
    balance_query = "SELECT payer, points FROM pointsdb;"
    balance = query_db(balance_query)

    print(balance)
    print("getting points")
    return "WIP"


########################
# Start Server
########################
if __name__ == "__main__":
    init_db()
    app.run(port = 8000)