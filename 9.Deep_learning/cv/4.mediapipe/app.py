import streamlit as st
import cv2
import mediapipe as mp
import tempfile

st.set_page_config(page_title="MediaPipe Demo", layout="wide")

# Sidebar options
st.sidebar.title("MediaPipe Features")
option = st.sidebar.selectbox(
    "Choose a Model",
    ["Face Detection", "Hand Tracking", "Face Mesh", "Pose Detection", "Holistic"]
)

st.title("🎥 MediaPipe Computer Vision Demo")
st.write("Select a feature from the sidebar and upload a video or use webcam.")

# File upload or Webcam option
source = st.sidebar.radio("Select Input Source", ["Webcam", "Upload Video"])

if source == "Upload Video":
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
else:
    uploaded_file = None

# Initialize MediaPipe solutions
mp_drawing = mp.solutions.drawing_utils
mp_face_detection = mp.solutions.face_detection
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

# Function to process frame
def process_frame(image, model):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if model == "Face Detection":
        with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as fd:
            results = fd.process(rgb)
            if results.detections:
                for detection in results.detections:
                    mp_drawing.draw_detection(image, detection)

    elif model == "Hand Tracking":
        with mp_hands.Hands() as hands:
            results = hands.process(rgb)
            if results.multi_hand_landmarks:
                for landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)

    elif model == "Face Mesh":
        with mp_face_mesh.FaceMesh() as fm:
            results = fm.process(rgb)
            if results.multi_face_landmarks:
                for landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(image, landmarks, mp_face_mesh.FACEMESH_TESSELATION)

    elif model == "Pose Detection":
        with mp_pose.Pose() as pose:
            results = pose.process(rgb)
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    elif model == "Holistic":
        with mp_holistic.Holistic() as holistic:
            results = holistic.process(rgb)
            if results.face_landmarks:
                mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)
            if results.left_hand_landmarks:
                mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            if results.right_hand_landmarks:
                mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

    return image

# Show video
stframe = st.empty()

if source == "Webcam":
    cap = cv2.VideoCapture(0)
else:
    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        cap = cv2.VideoCapture(tfile.name)
    else:
        cap = None

if cap is not None:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = process_frame(frame, option)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")

    cap.release()
