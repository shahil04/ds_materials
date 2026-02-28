import streamlit as st
from utilities import face_detection, hand_tracking, face_mesh, pose_detection, holistic_detection, volume_control

st.title("MediaPipe Utilities App")

menu = st.sidebar.selectbox("Choose a Utility", ["Face Detection", "Hand Tracking", "Face Mesh", "Pose Detection", "Holistic Detection", "Volume Control"])

if menu == "Face Detection":
    st.write("Run Face Detection")
    if st.button("Start Face Detection"):
        face_detection.run()

elif menu == "Hand Tracking":
    st.write("Run Hand Tracking")
    if st.button("Start Hand Tracking"):
        hand_tracking.run()

elif menu == "Face Mesh":
    st.write("Run Face Mesh Detection")
    if st.button("Start Face Mesh"):
        face_mesh.run()

elif menu == "Pose Detection":
    st.write("Run Pose Detection")
    if st.button("Start Pose Detection"):
        pose_detection.run()

elif menu == "Holistic Detection":
    st.write("Run Holistic Model Detection")
    if st.button("Start Holistic Detection"):
        holistic_detection.run()

elif menu == "Volume Control":
    st.write("Run Hand Gesture Volume Control")
    if st.button("Start Volume Control"):
        volume_control.run()
