from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS branches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    stock INTEGER,
                    price REAL,
                    supplier TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/branches')
def branches():
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute("SELECT * FROM branches")
    data = c.fetchall()
    conn.close()
    return render_template("branches.html", branches=data)

@app.route('/add-branch', methods=['GET', 'POST'])
def add_branch():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        conn = sqlite3.connect('clinic.db')
        c = conn.cursor()
        c.execute("INSERT INTO branches (name, description) VALUES (?, ?)", (name, description))
        conn.commit()
        conn.close()
        return redirect(url_for('branches'))
    return render_template("add_branch.html")

@app.route('/products')
def products():
    conn = sqlite3.connect('clinic.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    data = c.fetchall()
    conn.close()
    return render_template("products.html", products=data)

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        stock = request.form['stock']
        price = request.form['price']
        supplier = request.form['supplier']
        conn = sqlite3.connect('clinic.db')
        c = conn.cursor()
        c.execute("INSERT INTO products (name, category, stock, price, supplier) VALUES (?, ?, ?, ?, ?)",
                  (name, category, stock, price, supplier))
        conn.commit()
        conn.close()
        return redirect(url_for('products'))
    return render_template("add_product.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)