import cv2
import mediapipe as mp

def run():
    mp_holistic = mp.solutions.holistic
    holistic = mp_holistic.Holistic()
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, image = cap.read()
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = holistic.process(image_rgb)

        mp_draw.draw_landmarks(image, result.face_landmarks, mp_holistic.FACEMESH_TESSELATION)
        mp_draw.draw_landmarks(image, result.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_draw.draw_landmarks(image, result.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_draw.draw_landmarks(image, result.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

        cv2.imshow('Holistic Model', image)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
