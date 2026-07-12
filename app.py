from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("assetflow.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource_tag TEXT,
        start_time TEXT,
        end_time TEXT
    )
    """)

    conn.commit()
    conn.close()

# Home page - show all assets
@app.route("/")
def home():
    conn = sqlite3.connect("assetflow.db")
    cur = conn.cursor()

    cur.execute("SELECT tag, name, status FROM assets")
    assets = cur.fetchall()

    conn.close()
    return render_template("index.html", assets=assets)

# Add a new asset using a form
@app.route("/add_asset", methods=["POST"])
def add_asset():
    tag = request.form["tag"]
    name = request.form["name"]

    conn = sqlite3.connect("assetflow.db")
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO assets(tag, name, status) VALUES (?, ?, ?)",
            (tag, name, "Available")
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass

    conn.close()
    return redirect("/")

# Allocate an asset
@app.route("/allocate/<tag>")
def allocate(tag):
    conn = sqlite3.connect("assetflow.db")
    cur = conn.cursor()

    cur.execute("SELECT status FROM assets WHERE tag = ?", (tag,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return "Asset not found"

    if row[0] != "Available":
        conn.close()
        return "Asset already allocated"

    cur.execute(
        "UPDATE assets SET status = 'Allocated' WHERE tag = ?",
        (tag,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/book", methods=["POST"])
def book():
    resource = request.form["resource"]
    start = request.form["start"]
    end = request.form["end"]

    conn = sqlite3.connect("assetflow.db")
    cur = conn.cursor()

    # Get existing bookings for this resource
    cur.execute(
        "SELECT start_time, end_time FROM bookings WHERE resource_tag = ?",
        (resource,)
    )

    existing = cur.fetchall()

    new_start = datetime.fromisoformat(start)
    new_end = datetime.fromisoformat(end)

    # Overlap check
    for s, e in existing:
        old_start = datetime.fromisoformat(s)
        old_end = datetime.fromisoformat(e)

        if new_start < old_end and old_start < new_end:
            conn.close()
            return "Booking rejected: time slot overlaps!"

    # Save booking
    cur.execute(
        "INSERT INTO bookings(resource_tag, start_time, end_time) VALUES (?, ?, ?)",
        (resource, start, end)
    )

    conn.commit()
    conn.close()

    return "Booking created successfully!"

if __name__ == "__main__":
    init_db()
    app.run(debug=True)