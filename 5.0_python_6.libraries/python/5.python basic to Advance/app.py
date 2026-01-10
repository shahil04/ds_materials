# pip install streamlit
import streamlit as st

# -----------------------------
# In-memory database
# -----------------------------
if "students_db" not in st.session_state:
    st.session_state.students_db = {}

students_db = st.session_state.students_db

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("📚 Student Management")
menu = st.sidebar.radio(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

st.title("🎓 Student Management System (CRUD)")
st.write("Manage students using Create, Read, Update, Delete operations")

# -----------------------------
# CREATE
# -----------------------------
if menu == "Add Student":
    st.subheader("➕ Add Student")

    student_id = st.text_input("Student ID")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    course = st.text_input("Course")
    email = st.text_input("Email")

    if st.button("Add Student"):
        if student_id in students_db:
            st.error("❌ Student ID already exists!")
        else:
            students_db[student_id] = {
                "Name": name,
                "Age": age,
                "Course": course,
                "Email": email
            }
            st.success("✅ Student added successfully!")

# -----------------------------
# READ
# -----------------------------
elif menu == "View Students":
    st.subheader("📄 View All Students")

    if not students_db:
        st.warning("📭 No students found.")
    else:
        for sid, details in students_db.items():
            st.markdown(f"""
            **Student ID:** {sid}  
            **Name:** {details['Name']}  
            **Age:** {details['Age']}  
            **Course:** {details['Course']}  
            **Email:** {details['Email']}  
            ---
            """)

# -----------------------------
# UPDATE
# -----------------------------
elif menu == "Update Student":
    st.subheader("✏️ Update Student")

    student_id = st.text_input("Enter Student ID to Update")

    if student_id in students_db:
        name = st.text_input("Name", students_db[student_id]["Name"])
        age = st.number_input("Age", value=students_db[student_id]["Age"])
        course = st.text_input("Course", students_db[student_id]["Course"])
        email = st.text_input("Email", students_db[student_id]["Email"])

        if st.button("Update Student"):
            students_db[student_id] = {
                "Name": name,
                "Age": age,
                "Course": course,
                "Email": email
            }
            st.success("✅ Student updated successfully!")
    else:
        if student_id:
            st.error("❌ Student not found!")

# -----------------------------
# DELETE
# -----------------------------
elif menu == "Delete Student":
    st.subheader("🗑️ Delete Student")

    student_id = st.text_input("Enter Student ID to Delete")

    if st.button("Delete Student"):
        if student_id in students_db:
            del students_db[student_id]
            st.success("🗑️ Student deleted successfully!")
        else:
            st.error("❌ Student not found!")
