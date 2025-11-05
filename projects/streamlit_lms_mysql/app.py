
import streamlit as st
from db import create_database_and_tables, register_user, authenticate, seed_demo_data, get_connection
import db as dbmod
import os
import mysql.connector

st.set_page_config(page_title="LMS Portal", layout="wide")

# Initialize DB and seed
with st.spinner("Setting up database..."):
    try:
        create_database_and_tables()
        seed_demo_data()
    except Exception as e:
        st.error("DB setup/seed error: {}".format(e))

# Simple session management
if "user" not in st.session_state:
    st.session_state.user = None

# -- Helpers
def show_landing():
    st.markdown("""
    <div style='display:flex; justify-content:space-between; align-items:center'>
      <h1>📚 My Streamlit LMS</h1>
      <div>
        <a href='?page=login'><button style='padding:8px 12px;margin-right:8px'>Login</button></a>
        <a href='?page=register'><button style='padding:8px 12px'>Register</button></a>
      </div>
    </div>
    <hr/>
    """, unsafe_allow_html=True)
    st.markdown("""
    ### Learn anytime, anywhere.
    Choose a course and start learning.
    """)
    if st.button("Get Started"):
        st.experimental_set_query_params(page="register")

def show_register():
    st.header("Create an account")
    with st.form("reg"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        password2 = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Register")
        if submitted:
            if not username or not password or password!=password2:
                st.warning("Please fill fields and ensure passwords match.")
            else:
                ok, err = register_user(username, email, password)
                if ok:
                    st.success("Account created. Please login.")
                    st.experimental_set_query_params(page="login")
                else:
                    st.error("Registration error: {}".format(err))

def show_login():
    st.header("Login to your account")
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            user = authenticate(username, password)
            if user:
                st.session_state.user = user
                st.success("Logged in as {}".format(user['username']))
                st.experimental_set_query_params(page="courses")
            else:
                st.error("Invalid credentials.")

def show_courses():
    st.sidebar.title("Navigation")
    st.sidebar.write("Logged in as: **{}**".format(st.session_state.user['username']))
    cnx = get_connection()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    cursor.close(); cnx.close()

    st.header("Courses")
    cols = st.columns(2)
    for i, c in enumerate(courses):
        col = cols[i%2]
        with col:
            st.image(c['thumbnail'] if c['thumbnail'] else None, width=300)
            st.subheader(c['title'])
            st.write(c['description'])
            if st.button("View Course", key=f"view_{c['id']}"):
                st.experimental_set_query_params(page="course", course_id=c['id'])

def show_course_detail(course_id:int):
    # fetch course, modules, videos
    cnx = get_connection()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses WHERE id=%s", (course_id,))
    course = cursor.fetchone()
    cursor.execute("SELECT * FROM modules WHERE course_id=%s ORDER BY ordering", (course_id,))
    modules = cursor.fetchall()
    # sidebar modules list
    st.sidebar.header(course['title'])
    for m in modules:
        with st.sidebar.expander(m['title']):
            cursor.execute("SELECT * FROM videos WHERE module_id=%s ORDER BY ordering", (m['id'],))
            vids = cursor.fetchall()
            for v in vids:
                # show small entry
                st.write(f"- [{v['title']}](?page=course&course_id={course_id}&video_id={v['id']})")


    st.title(course['title'])
    # if video selected
    query = st.experimental_get_query_params()
    vid_id = int(query.get("video_id",[0])[0]) if query.get("video_id") else None
    if vid_id:
        cursor.execute("SELECT * FROM videos WHERE id=%s", (vid_id,))
        video = cursor.fetchone()
        st.subheader(video['title'])
        # embed youtube
        st.video(video['youtube_link'])

        tabs = st.tabs(["Attachment","Notes","Rating"])
        with tabs[1]:
            # notes: load & save to DB
            cursor.execute("SELECT note FROM notes WHERE user_id=%s AND video_id=%s", (st.session_state.user['id'], vid_id))
            r = cursor.fetchone()
            current = r['note'] if r else ""
            txt = st.text_area("Your notes", value=current, height=200)
            if st.button("Save Note", key=f"note_{vid_id}"):
                # upsert
                if r:
                    cursor.execute("UPDATE notes SET note=%s WHERE user_id=%s AND video_id=%s", (txt, st.session_state.user['id'], vid_id))
                else:
                    cursor.execute("INSERT INTO notes (user_id, video_id, note) VALUES (%s,%s,%s)", (st.session_state.user['id'], vid_id, txt))
                cnx.commit()
                st.success("Saved")
        with tabs[2]:
            cursor.execute("SELECT rating FROM ratings WHERE user_id=%s AND video_id=%s", (st.session_state.user['id'], vid_id))
            r2 = cursor.fetchone()
            current_rating = r2['rating'] if r2 else 3
            rating = st.slider("Rate this video", 1, 5, value=current_rating, key=f"rate_{vid_id}")
            if st.button("Save Rating", key=f"save_rate_{vid_id}"):
                if r2:
                    cursor.execute("UPDATE ratings SET rating=%s WHERE user_id=%s AND video_id=%s", (rating, st.session_state.user['id'], vid_id))
                else:
                    cursor.execute("INSERT INTO ratings (user_id, video_id, rating) VALUES (%s,%s,%s)", (st.session_state.user['id'], vid_id, rating))
                cnx.commit()
                st.success("Rating saved")
        # mark as complete
        completed = False
        cursor.execute("SELECT completed FROM progress WHERE user_id=%s AND video_id=%s", (st.session_state.user['id'], vid_id))
        r3 = cursor.fetchone()
        if r3:
            completed = bool(r3['completed'])
        chk = st.checkbox("Mark as Complete", value=completed)
        if st.button("Save Progress", key=f"prog_{vid_id}"):
            if r3:
                cursor.execute("UPDATE progress SET completed=%s WHERE user_id=%s AND video_id=%s", (chk, st.session_state.user['id'], vid_id))
            else:
                cursor.execute("INSERT INTO progress (user_id, video_id, completed) VALUES (%s,%s,%s)", (st.session_state.user['id'], vid_id, chk))
            cnx.commit()
            st.success("Progress updated")
    else:
        st.info("Select a video from the sidebar modules to start.")

    # progress bar (simple): percent of videos completed
    cursor.execute("SELECT COUNT(*) total FROM videos WHERE module_id IN (SELECT id FROM modules WHERE course_id=%s)", (course_id,))
    total = cursor.fetchone()['total'] or 0
    cursor.execute("SELECT COUNT(*) done FROM progress WHERE user_id=%s AND completed=1 AND video_id IN (SELECT id FROM videos WHERE module_id IN (SELECT id FROM modules WHERE course_id=%s))", (st.session_state.user['id'], course_id))
    done = cursor.fetchone()['done'] or 0
    pct = int((done/total)*100) if total>0 else 0
    st.progress(pct/100)
    st.caption(f"Course Progress: {pct}%")

    cursor.close(); cnx.close()

# -- Router
query = st.experimental_get_query_params()
page = query.get("page", ["home"])[0]

if page == "home":
    show_landing()
elif page == "register":
    show_register()
elif page == "login":
    show_login()
elif page == "courses":
    if st.session_state.user:
        show_courses()
    else:
        st.warning("Please login first.")
        st.experimental_set_query_params(page="login")
elif page == "course":
    if st.session_state.user:
        cid = int(query.get("course_id",[0])[0])
        show_course_detail(cid)
    else:
        st.warning("Please login first.")
        st.experimental_set_query_params(page="login")
else:
    show_landing()
