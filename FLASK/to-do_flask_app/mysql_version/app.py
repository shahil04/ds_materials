from flask import Flask, render_template, request,redirect,url_for,flash
from db import get_db_connection

app = Flask(__name__)
app.secret_key ="secret123"   # Required for flash messages

# Ensure DB is initialized
# init_db()


@app.route("/")
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM todos")
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', tasks=tasks)

    
    
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    if task.strip() == "":
        flash("Task cannot be empty!", "error")
        return redirect(url_for('index'))

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
    
    connection.commit()
    cursor.close()
    connection.close()
    flash("Task added successfully!", "success")
    return redirect(url_for('index'))


@app.route('/update/<int:id>')
def update_task(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE todos SET status='Completed' WHERE id=%s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    flash("Task marked as completed!", "success")
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_task(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM todos WHERE id=%s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    flash("Task deleted successfully!", "success")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
