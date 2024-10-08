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
        init_points_query = "CREATE TABLE IF NOT EXISTS points_db(payer TEXT, points INTEGER, timestamp TEXT);"
        query_db(init_points_query)

    return

# From Flask Documentation https://flask.palletsprojects.com/en/3.0.x/patterns/sqlite3/
def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    results = cur.fetchall()
    db.commit()
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
    
    add_query = "INSERT INTO points_db VALUES (?, ?, ?);"
    try:
        query_db(add_query, [
            request_json["payer"], 
            request_json["points"], 
            request_json["timestamp"]])
        return "", 200
    except Error as e:
        return "Error adding points", 500


@app.route("/spend", methods=['POST'])
def spend_points():
    print("spending points")

    request_json = request.get_json()

    # Check that the json has the data we need
    if ("points" not in request_json.keys()):
        return "Invalid JSON", 400

    points_to_spend = request_json["points"]
    
    # Check if there are enough points to spend
    total_balance_query = "SELECT SUM(points) FROM points_db"
    total_balance = query_db(total_balance_query)[0][0]

    if (total_balance < points_to_spend):
        return "Insufficient points", 400

    # Keep track of the ones we spend
    running_total = dict()

    while points_to_spend > 0:
        # Makes sure we get the oldest query that isn't 0
        # Have to keep 0s to make sure we still display payers with 0 points in /balance
        oldest_query = "SELECT * FROM points_db WHERE points != 0 ORDER BY timestamp ASC;"
        oldest_points = query_db(oldest_query, one = True)

        # Make sure we can keep track of who's points we spent
        if (oldest_points[0] not in running_total.keys()):
            running_total[oldest_points[0]] = 0

        if (oldest_points[1] > points_to_spend):
            # Not all points will be spent
            update_query = "UPDATE points_db SET points = ? WHERE payer = ? AND points = ? AND timestamp = ?;"
            query_db(update_query, [
                oldest_points[1] - points_to_spend,
                oldest_points[0],
                oldest_points[1],
                oldest_points[2]])

            # Update how much we spent for a given buyer
            running_total[oldest_points[0]] -= points_to_spend
            # If we're not spending all of the points, we're done spending
            return
        else:
            # Set entry in points_db to 0
            update_query = "UPDATE points_db SET points = ? WHERE payer = ? AND points = ? AND timestamp = ?;"
            query_db(update_query, [
                0,
                oldest_points[0],
                oldest_points[1],
                oldest_points[2]])

            # Update how much we spent for a given buyer
            running_total[oldest_points[0]] -= oldest_points[1]
            # Update the ammount we still need to spend 
            points_to_spend -= oldest_points[1]

    return jsonify(running_total), 200

@app.route("/balance", methods=['GET'])
def get_balance():
    balance_query = "SELECT payer, SUM(points) FROM points_db GROUP BY payer;"
    balance = query_db(balance_query)

    print(balance)
    return jsonify(balance), 200


########################
# Start Server
########################
if __name__ == "__main__":
    init_db()
    app.run(port = 8000)