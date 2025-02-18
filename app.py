from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'kanban'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'
mongo = PyMongo(app)

# @app.route('/')
# def home():
#     if 'username' in session:
#         return redirect(url_for('profile'))
#     return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mongo.db.users.find_one({'username': username})
        print([i for x in mongo.db.data.find({})])
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            flash('Invalid credentials. Please try again.')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({'username': username, 'password': hashed_password})
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)