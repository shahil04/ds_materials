import cv2
import mediapipe as mp

def run():
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh()
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image_rgb)

        if results.multi_face_landmarks:
            for landmarks in results.multi_face_landmarks:
                mp_draw.draw_landmarks(image, landmarks, mp_face_mesh.FACEMESH_TESSELATION)

        cv2.imshow('Face Mesh', image)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
