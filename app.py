from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login_page.html')  # Ensure this file exists in `templates/`

@app.route('/registration_page')
def registration_page():
    return render_template('registration_page.html')  # Ensure this file exists in `templates/`

if __name__ == '__main__':
    app.run(debug=True)
