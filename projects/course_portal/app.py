from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM modules")
    modules = cursor.fetchall()
    conn.close()
    return render_template('index.html', modules=modules, user_role=session.get('role'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                       (name, email, password, role))
        conn.commit()
        conn.close()
        flash("Registration successful! Please login.", "success")
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['role'] = user['role']
            flash("Login successful!", "success")
            return redirect('/')
        else:
            flash("Invalid credentials!", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/module/<int:module_id>')
def module(module_id):
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM modules WHERE id=%s", (module_id,))
    module = cursor.fetchone()

    cursor.execute("SELECT c.comment, c.created_at, u.name FROM comments c JOIN users u ON c.user_id=u.id WHERE c.module_id=%s ORDER BY c.created_at DESC", (module_id,))
    comments = cursor.fetchall()
    conn.close()
    return render_template('module.html', module=module, comments=comments)

@app.route('/comment/<int:module_id>', methods=['POST'])
def comment(module_id):
    if 'user_id' not in session:
        return redirect('/login')
    comment = request.form['comment']
    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (module_id, user_id, comment) VALUES (%s, %s, %s)", (module_id, user_id, comment))
    conn.commit()
    conn.close()
    return redirect(url_for('module', module_id=module_id))

if __name__ == '__main__':
    app.run(debug=True)
