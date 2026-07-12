from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("assetflow.db")
    cur = conn.cursor()

    # Assets table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag TEXT UNIQUE,
        name TEXT,
        status TEXT
    )
    """)

    # Bookings table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource_tag TEXT,
        start_time TEXT,
        end_time TEXT
    )
    """)

    # Employees table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE
    )
    """)
    # Allocations table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS allocations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_tag TEXT,
        employee_email TEXT
    )
    """)
    # Maintenance requests table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS maintenance_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_tag TEXT,
        issue TEXT,
        status TEXT
    )
    """)
    conn.commit()
    conn.close()

# Home page - show all assets
@app.route("/")
def home():
    conn = sqlite3.connect("assetflow.db")
    cur = conn.cursor()

    # Assets
    cur.execute("SELECT tag, name, status FROM assets")
    assets = cur.fetchall()

    # Bookings
    cur.execute("SELECT resource_tag, start_time, end_time FROM bookings")
    bookings = cur.fetchall()

    # Employees
    cur.execute("SELECT name, email FROM employees")
    employees = cur.fetchall()

    # Dashboard stats
    cur.execute("SELECT COUNT(*) FROM assets")
    total_assets = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM assets WHERE status = 'Available'")
    available_assets = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM assets WHERE status = 'Allocated'")
    allocated_assets = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM employees")
    total_employees = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cur.fetchone()[0]
    
    cur.execute("SELECT asset_tag, issue, status FROM maintenance_requests")
    maintenance_requests = cur.fetchall()
    conn.close()

    return render_template(
        "index.html",
        assets=assets,
        bookings=bookings,
        employees=employees,
        total_assets=total_assets,
        available_assets=available_assets,
        allocated_assets=allocated_assets,
        total_employees=total_employees,
        total_bookings=total_bookings,
        maintenance_requests=maintenance_requests,
    )
# Add a new asset using a form
@app.route("/add_asset", methods=["POST"])
def add_asset():
    tag = request.form["tag"]
    name = request.form["name"]

    conn = sqlite3.connect("assetflow.db")
    cur = conn.cursor()

    # If the asset already exists, make it Available again
    cur.execute("SELECT id FROM assets WHERE tag = ?", (tag,))
    existing = cur.fetchone()

    if existing:
        cur.execute(
            "UPDATE assets SET name = ?, status = 'Available' WHERE tag = ?",
            (name, tag)
        )
    else:
        cur.execute(
            "INSERT INTO assets(tag, name, status) VALUES (?, ?, ?)",
            (tag, name, "Available")
        )

    conn.commit()
    conn.close()

    return redirect("/")
# Allocate an asset
@app.route("/allocate/<tag>/<email>")
def allocate(tag, email):
    conn = sqlite3.connect("assetflow.db")
    cur = conn.cursor()

    # Check asset status
    cur.execute("SELECT status FROM assets WHERE tag = ?", (tag,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return "Asset not found"

    if row[0] != "Available":
        conn.close()
        return "Asset already allocated"

    # Record allocation
    cur.execute(
        "INSERT INTO allocations(asset_tag, employee_email) VALUES (?, ?)",
        (tag, email)
    )

    # Update asset status
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
@app.route("/add_employee", methods=["POST"])
def add_employee():
    name = request.form["name"]
    email = request.form["email"]

    conn = sqlite3.connect("assetflow.db")
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO employees(name, email) VALUES (?, ?)",
            (name, email)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass

    conn.close()
    return redirect("/")
@app.route("/raise_maintenance", methods=["POST"])
def raise_maintenance():
    asset_tag = request.form["asset_tag"]
    issue = request.form["issue"]

    conn = sqlite3.connect("assetflow.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO maintenance_requests(asset_tag, issue, status) VALUES (?, ?, ?)",
        (asset_tag, issue, "Pending")
    )

    conn.commit()
    conn.close()

    return redirect("/")
if __name__ == "__main__":
    init_db()
    app.run(debug=True)