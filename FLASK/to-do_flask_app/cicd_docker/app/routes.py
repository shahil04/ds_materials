from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db import get_db_connection

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@todo_bp.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if not task.strip():
        flash("Task cannot be empty!", "error")
        return redirect(url_for('todo.index'))

    conn = get_db_connection()
    conn.execute('INSERT INTO todos (task) VALUES (?)', (task,))
    conn.commit()
    conn.close()
    flash("Task added successfully!", "success")
    return redirect(url_for('todo.index'))

@todo_bp.route('/update/<int:id>')
def update_task(id):
    conn = get_db_connection()
    conn.execute('UPDATE todos SET status="Completed" WHERE id=?', (id,))
    conn.commit()
    conn.close()
    flash("Task marked as completed!", "success")
    return redirect(url_for('todo.index'))

@todo_bp.route('/delete/<int:id>')
def delete_task(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM todos WHERE id=?', (id,))
    conn.commit()
    conn.close()
    flash("Task deleted successfully!", "success")
    return redirect(url_for('todo.index'))
