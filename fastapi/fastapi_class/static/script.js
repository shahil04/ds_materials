const todoInput = document.getElementById('todo-input');
const serialInput = document.getElementById('serial-input');
const timeInput = document.getElementById('time-input');
const dateInput = document.getElementById('date-input');
const addBtn = document.getElementById('add-btn');
const todoList = document.getElementById('todo-list');

const API_URL = '/api/todos';

// Theme toggle logic
const themeToggleBtn = document.getElementById('theme-toggle');
const body = document.body;

// Check local storage
const currentTheme = localStorage.getItem('theme');
if (currentTheme) {
    body.setAttribute('data-theme', currentTheme);
}

if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
        if (body.getAttribute('data-theme') === 'light') {
            body.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            body.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    });
}

// Set default date to today
const today = new Date().toISOString().split('T')[0];
if (dateInput) dateInput.value = today;

// Fetch and display todos on load
document.addEventListener('DOMContentLoaded', fetchTodos);

// Add todo on button click or Enter key
if (addBtn) addBtn.addEventListener('click', addTodo);
if (todoInput) {
    todoInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addTodo();
    });
}

async function fetchTodos() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error('Failed to fetch');
        const todos = await response.json();
        todoList.innerHTML = '';
        todos.forEach(renderTodo);
    } catch (error) {
        console.error('Error fetching todos:', error);
    }
}

async function addTodo() {
    const title = todoInput.value.trim();
    const serial = serialInput.value.trim();
    const date = dateInput.value;
    const time = timeInput.value;

    if (!title) {
        alert("Please enter a task description");
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: title,
                serial_number: serial || "",
                due_date: date || "",
                due_time: time || ""
            })
        });

        if (!response.ok) {
            console.error('Error adding todo:', await response.text());
            return;
        }

        const newTodo = await response.json();
        renderTodo(newTodo);

        // Clear inputs
        todoInput.value = '';
        serialInput.value = '';
        timeInput.value = '';
        // Reset date to today
        dateInput.value = today;
    } catch (error) {
        console.error('Error adding todo:', error);
    }
}

async function toggleTodo(id, currentStatus, title, serial, date, time) {
    if (id === undefined || id === null) {
        console.error("Error: Todo ID is undefined");
        return;
    }

    // Convert strings 'null' or 'undefined' back to empty strings if necessary, though escapeHtml handles display
    // We send back exactly what we received (or safe defaults) to satisfy the schema
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: title || "",
                completed: !currentStatus,
                serial_number: serial || "",
                due_date: date || "",
                due_time: time || ""
            })
        });

        if (response.ok) {
            fetchTodos();
        } else {
            console.error('Error updating todo:', await response.text());
        }
    } catch (error) {
        console.error('Error updating todo:', error);
    }
}

async function deleteTodo(id) {
    if (!confirm('Are you sure you want to delete this task?')) return;
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });
        if (response.ok) {
            const item = document.querySelector(`li[data-id="${id}"]`);
            if (item) {
                item.style.opacity = '0';
                item.style.transform = 'translateX(20px)';
                setTimeout(() => item.remove(), 300);
            } else {
                fetchTodos();
            }
        }
    } catch (error) {
        console.error('Error deleting todo:', error);
    }
}

function renderTodo(todo) {
    const li = document.createElement('li');
    li.dataset.id = todo.id;
    if (todo.completed) li.classList.add('completed');

    const safeTitle = escapeHtml(todo.title || "");
    const safeSerial = todo.serial_number ? escapeHtml(todo.serial_number) : '';
    const safeDate = todo.due_date ? escapeHtml(todo.due_date) : '';
    const safeTime = todo.due_time ? escapeHtml(todo.due_time) : '';

    // We must pass arguments as strings with quotes for the JS function
    // We replace existing single quotes to escape them in the function call
    const cleanTitle = (todo.title || "").replace(/'/g, "\\'");
    const cleanSerial = (todo.serial_number || "").replace(/'/g, "\\'");
    const cleanDate = (todo.due_date || "").replace(/'/g, "\\'");
    const cleanTime = (todo.due_time || "").replace(/'/g, "\\'");

    li.innerHTML = `
        <div class="todo-content" onclick="toggleTodo(${todo.id}, ${todo.completed}, '${cleanTitle}', '${cleanSerial}', '${cleanDate}', '${cleanTime}')">
            <div class="checkbox"></div>
            ${safeSerial ? `<span class="serial-no">#${safeSerial}</span>` : ''}
            <div class="todo-details">
                <span class="todo-text">${safeTitle}</span>
                <div class="todo-meta">
                    ${safeDate ? `<span>📅 ${safeDate}</span>` : ''}
                    ${safeTime ? `<span>⏰ ${safeTime}</span>` : ''}
                </div>
            </div>
        </div>
        <button class="delete-btn" onclick="deleteTodo(${todo.id})">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
        </button>
    `;

    // Add to top of list
    todoList.prepend(li);
}

function escapeHtml(text) {
    if (text === null || text === undefined) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
