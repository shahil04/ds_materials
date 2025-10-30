import streamlit as st
import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="course_portal"
    )

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("🎓 Course Admin Dashboard")

admin_email = st.text_input("Admin Email")
admin_pass = st.text_input("Password", type="password")
login_btn = st.button("Login")

if login_btn:
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s AND role='admin'", (admin_email,))
    admin = cursor.fetchone()
    if admin:
        st.success(f"Welcome {admin['name']}!")
        st.session_state['admin_logged_in'] = True
    else:
        st.error("Invalid credentials or not an admin.")

if st.session_state.get('admin_logged_in', False):
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Add Module", "View Modules"])

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if page == "Add Module":
        st.subheader("➕ Add New Module")
        title = st.text_input("Title")
        youtube = st.text_input("YouTube Embed Link")
        notes = st.text_input("Google Docs Notes Link")
        desc = st.text_area("Description")
        if st.button("Add Module"):
            cursor.execute("INSERT INTO modules (title, youtube_link, notes_link, description) VALUES (%s, %s, %s, %s)", (title, youtube, notes, desc))
            conn.commit()
            st.success("Module added successfully!")

    elif page == "View Modules":
        cursor.execute("SELECT * FROM modules")
        data = cursor.fetchall()
        st.table(data)
