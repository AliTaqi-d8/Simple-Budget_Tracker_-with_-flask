from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Initialize database
DATABASE = "budget.db"

def init_db():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              category TEXT NOT NULL,
                              amount REAL NOT NULL,
                              description TEXT NOT NULL)''')
            conn.commit()

@app.route('/')
def index():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0] or 0
    return render_template("index.html", expenses=expenses, total=total)

@app.route('/add', methods=['POST'])
def add_expense():
    category = request.form['category']
    amount = float(request.form['amount'])
    description = request.form['description']

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (category, amount, description) VALUES (?, ?, ?)", 
                       (category, amount, description))
        conn.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:expense_id>')
def delete_expense(expense_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
