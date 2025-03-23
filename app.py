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

@app.route('/')
def home():
    return render_template('index.html') 

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

if __name__ == '__main__':
    app.run(debug=True)
