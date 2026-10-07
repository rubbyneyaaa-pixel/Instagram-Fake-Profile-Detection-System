from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# =========================
# HOME PAGE
# =========================

@app.route('/')
def home():
    return render_template('index.html')


# =========================
# REGISTER PAGE
# =========================

@app.route('/register', methods=['GET', 'POST'])
def register():

    message = ""

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            password TEXT
        )
        """)

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        message = "Registration Successful!"

    return render_template(
        'register.html',
        message=message
    )


# =========================
# LOGIN PAGE
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    message = ""

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            message = "Login Successful!"
        else:
            message = "Invalid Email or Password"

    return render_template(
        'login.html',
        message=message
    )


# =========================
# DASHBOARD + SEARCH USER
# =========================

@app.route('/dashboard')
def dashboard():

    search = request.args.get('search', '')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id,name,email FROM users WHERE name LIKE ?",
        ('%' + search + '%',)
    )

    users = cursor.fetchall()

    conn.close()

    return render_template(
        'dashboard.html',
        users=users,
        search=search
    )


# =========================
# DELETE USER
# =========================

@app.route('/delete/<int:user_id>')
def delete_user(user_id):

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')


# =========================
# PROFILE DETECTION
# =========================

@app.route('/detection', methods=['GET', 'POST'])
def detection():

    result = ""

    if request.method == 'POST':

        username = request.form['username']
        insta_id = request.form['insta_id']

        followers = int(request.form['followers'])
        following = int(request.form['following'])
        posts = int(request.form['posts'])
        bio = int(request.form['bio'])

        if followers < 100 and following > 1000 and posts < 10:
            result = "Fake Profile"
        else:
            result = "Genuine Profile"

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO history(username, insta_id, result)
        VALUES (?, ?, ?)
        """, (username, insta_id, result))

        conn.commit()
        conn.close()

    return render_template(
        'detection.html',
        result=result
    )


# =========================
# HISTORY PAGE
# =========================

@app.route('/history')
def history():

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM history"
    )

    records = cursor.fetchall()

    conn.close()

    return render_template(
        'history.html',
        records=records
    )


# =========================
# RUN APP
# =========================

if __name__ == '__main__':
    app.run(debug=True)