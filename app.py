from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
DB = "notes.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# create table once
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    """)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/notes", methods=["GET"])
def get_notes():
    db = get_db()
    notes = db.execute("SELECT * FROM notes").fetchall()
    return jsonify([dict(n) for n in notes])

@app.route("/notes", methods=["POST"])
def add_note():
    data = request.json
    db = get_db()
    db.execute("INSERT INTO notes (text) VALUES (?)", (data["text"],))
    db.commit()
    return jsonify({"status": "ok"})

@app.route("/notes/<int:id>", methods=["PUT"])
def update_note(id):
    data = request.json
    db = get_db()
    db.execute("UPDATE notes SET text=? WHERE id=?", (data["text"], id))
    db.commit()
    return jsonify({"status": "ok"})

@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    db = get_db()
    db.execute("DELETE FROM notes WHERE id=?", (id,))
    db.commit()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
