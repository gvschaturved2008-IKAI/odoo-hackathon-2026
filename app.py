from flask import Flask
import sqlite3

app = Flask(__name__)

# Create the database and assets table
def init_db():
    conn = sqlite3.connect("assetflow.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag TEXT UNIQUE,
        name TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

# Home page
@app.route("/")
def home():
    return """
    <h1>AssetFlow</h1>
    <p>Hackathon project is running!</p>
    <a href='/add_asset'>Add Sample Asset</a><br><br>
    <a href='/allocate'>Allocate Asset</a>
    """

# Add a sample asset
@app.route("/add_asset")
def add_asset():
    conn = sqlite3.connect("assetflow.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO assets(tag, name, status) VALUES (?, ?, ?)",
        ("AF-0001", "Dell Laptop", "Available")
    )

    conn.commit()
    conn.close()

    return "Sample asset added successfully!"

# Allocate the asset
@app.route("/allocate")
def allocate():
    conn = sqlite3.connect("assetflow.db")
    cur = conn.cursor()

    cur.execute("SELECT status FROM assets WHERE tag = ?", ("AF-0001",))
    row = cur.fetchone()

    if not row:
        conn.close()
        return "Asset not found"

    if row[0] != "Available":
        conn.close()
        return "Asset already allocated"

    cur.execute(
        "UPDATE assets SET status = 'Allocated' WHERE tag = ?",
        ("AF-0001",)
    )

    conn.commit()
    conn.close()

    return "Asset allocated successfully!"

if __name__ == "__main__":
    init_db()
    app.run(debug=True)