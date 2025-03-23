from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('cart.html')  

@app.route('/registration_page')
def registration_page():
    return render_template('registration_page.html')  

@app.route('/forgot_password_page')
def forgot_password_page():
    return render_template('forgot_password_page.html')  

if __name__ == '__main__':
    app.run(debug=True)
