import os
import sqlite3
from flask import Flask, flash, redirect, render_template, jsonify, request, session, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Configure application
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Function to get the database connection for each request
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

# Close the database connection after each request
@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
def home():
    return render_template('sofas.html') 

@app.route("/cart_page")
@login_required
def cart_page():
    """Render the cart page"""
    return redirect("/cart") 

@app.route("/shop")

def shop_page():
    """Render the shop page"""
    return render_template("all.html")

@app.route("/about")

def about_page():
    """Render the about page"""
    return render_template("about_page.html")

@app.route("/journal")

def journal_page():
    """Render the journal page"""
    return render_template("journal.html")

@app.route("/contact")

def contact_page():
    """Render the contact page"""
    return render_template("contact.html")

@app.route('/registration_page')
def registration_page():
    return render_template('registration_page.html')  

@app.route('/forgot_password_page')
def forgot_password_page():
    return render_template('forgot_password_page.html') 

# navigation links for product shop page 
@app.route("/all")

def shop_all_page():
    """Render the journal page"""
    return render_template("all.html")

@app.route("/beds")

def shop_beds_page():
    """Render the journal page"""
    return render_template("shop_beds.html")

@app.route("/home_decor")

def shop_home_decor_page():
    """Render the journal page"""
    return render_template("home_decor.html")

@app.route("/dining_set")

def shop_dining_set_page():
    """Render the journal page"""
    return render_template("dining_set.html")

@app.route("/sofas")

def shop_sofas_page():
    """Render the journal page"""
    return render_template("sofas.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username", 403)
        elif not password:
            return apology("must provide password", 403)

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user is None or not check_password_hash(user["hash"], password):
            return apology("invalid username and/or password", 403)

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect("/")

    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif password != confirm_password:
            return apology("passwords do not match", 400)

        db = get_db()
        if db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone():
            return apology("username already exists", 400)

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (username, generate_password_hash(password)))
        db.commit()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        session["user_id"] = user["id"]
        session["username"] = username
        return redirect("/")

    return render_template("register.html")

# Change password
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change user password"""
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        db = get_db()
        user = db.execute("SELECT hash FROM users WHERE id = ?", (session["user_id"],)).fetchone()

        if not user or not check_password_hash(user["hash"], current_password):
            return apology("Invalid current password", 400)
        if new_password != confirm_password:
            return apology("Passwords do not match", 400)

        db.execute("UPDATE users SET hash = ? WHERE id = ?", (generate_password_hash(new_password), session["user_id"]))
        db.commit()
        flash("Password successfully changed", "success")
        return redirect("/")

    return render_template("change_password.html")

# Product page
@app.route("/product/<int:product_id>")
def product_page(product_id):
    """Display a single product"""
    conn = get_db()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    images = conn.execute('SELECT image FROM product_images WHERE product_id = ?', (product_id,)).fetchall()

    if not product:
        return "Product not found", 404

    return render_template('product.html', product=product, images=[image['image'] for image in images])



if __name__ == '__main__':
    app.run(debug=True)
