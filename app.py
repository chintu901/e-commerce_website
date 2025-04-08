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
@login_required
def home():
    return render_template("admin_layout.html")

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
@login_required
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

    return render_template("login_page.html")

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

    return render_template("registration_page.html")

# Forgot password
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    """Handle password reset process"""
    if request.method == "POST":
        username = request.form.get("username")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        db = get_db()
        user = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()

        if not user:
            return apology("Username not found", 400)

        if new_password and confirm_password:
            if new_password != confirm_password:
                return apology("Passwords do not match", 400)
            
            db.execute("UPDATE users SET hash = ? WHERE id = ?", 
                       (generate_password_hash(new_password), user["id"]))
            db.commit()
            flash("Password successfully reset", "success")
            return redirect("/login")
        
    return render_template("forgot_password.html")


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

@app.route("/profile")
@login_required
def profile():
    """Render the profile page"""
    username = session.get('username')
    return render_template('profile.html', username=username)

@app.route("/cart")
@login_required
def cart():
    """Render the cart page with items for the logged-in user"""
    user_id = session.get("user_id")
    if not user_id:
        return "Please log in to view your cart", 401

    # Get a database connection and retrieve cart items
    db = get_db()
    cart_items = db.execute(
        "SELECT * FROM cart_items WHERE user_id = ?", (user_id,)
    ).fetchall()

    # Debugging print statement (can be removed later)
    print("Cart items:", cart_items)

    return render_template("cart.html", cart_items=cart_items)

@app.route("/checkout")
@login_required
def checkout():
    user_id = session.get("user_id")
    print("User ID from session:", user_id)

    if not user_id:
        return "Please log in to view the checkout page", 401

    db = get_db()
    cart_items = db.execute(
        "SELECT * FROM cart_items WHERE user_id = ?", (user_id,)
    ).fetchall()

    print("Checkout items:", cart_items)

    # Convert to dicts
    cart_items = [dict(row) for row in cart_items]

    return render_template("check_out.html", cart_items=cart_items)


# Cart count
@app.before_request
def load_cart_count():
    if "user_id" in session:
        db = get_db()
        user_id = session["user_id"]
        cart_count = db.execute(
            "SELECT COUNT(*) FROM cart_items WHERE user_id = ?", (user_id,)
        ).fetchone()[0]
        g.cart_count = cart_count  # Store in `g` for global access
    else:
        g.cart_count = 0  # No items if not logged in

@app.route("/add_to_cart", methods=["POST"])
@login_required
def add_to_cart():
    """Add a product to the user's cart in the database"""
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("quantity", 1))
    user_id = session["user_id"]

    # Ensure product_id is provided
    if not product_id:
        return apology("Product ID is required", 400)

    # Connect to the database
    db = get_db()
    
    # Check if the product already exists in the user's cart
    existing_cart_item = db.execute(
        "SELECT * FROM cart WHERE user_id = ? AND product_id = ?",
        (user_id, product_id)
    ).fetchone()

    if existing_cart_item:
        # Update the quantity of the existing cart item
        db.execute(
            "UPDATE cart SET quantity = quantity + ? WHERE user_id = ? AND product_id = ?",
            (quantity, user_id, product_id)
        )
    else:
        # Insert a new item into the cart
        db.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
            (user_id, product_id, quantity)
        )
    
    db.commit()
    flash("Item added to cart", "success")
    return redirect("/cart_page")

@app.route("/remove_item", methods=["POST"])
@login_required
def remove_item():
    """Remove an item from the cart"""
    product_id = request.form.get("product_id")
    user_id = session.get("user_id")

    if not product_id or not user_id:
        return "Invalid request", 400

    db = get_db()
    db.execute("DELETE FROM cart WHERE user_id = ? AND product_id = ?", (user_id, product_id))
    db.commit()

    flash("Item removed from cart", "success")

    # Redirect to the referring page (check_out or cart)
    return redirect(request.referrer or "/cart")

@app.route("/total_price")
@login_required
def total_price():
    """Calculate and return the total price of items in the cart"""
    user_id = session.get("user_id")
    if not user_id:
        return "Please log in to view your cart", 401

    # Get a database connection and retrieve cart items
    db = get_db()
    cart_items = db.execute(
        "SELECT p.price, c.quantity FROM cart c JOIN products p ON c.product_id = p.id WHERE c.user_id = ?",
        (user_id,)
    ).fetchall()

    # Calculate total price
    total_price = sum(item["price"] * item["quantity"] for item in cart_items)

    return str(total_price)  # Return total price as string

@app.route("/cart_count")
@login_required
def cart_count():
    """Return the count of items in the cart for the logged-in user"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify(count=0)  # Return zero if no user is logged in

    db = get_db()
    # Fetch the cart count from the database
    cart_count = db.execute(
        "SELECT COUNT(*) FROM cart_items WHERE user_id = ?", (user_id,)
    ).fetchone()[0]

    # Return the count as JSON
    return jsonify(count=cart_count)

if __name__ == '__main__':
    app.run(debug=True)
