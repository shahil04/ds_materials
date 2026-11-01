from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import cv2
import mediapipe as mp
import numpy as np
import base64, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "exam_secret_key_123"   # change in production
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
EVIDENCE_DIR = os.path.join(PROJECT_ROOT, "static", "evidence")
os.makedirs(EVIDENCE_DIR, exist_ok=True)

# Candidate & Exam Metadata
CANDIDATE_INFO = {
    "name": "Alex Morgan",
    "roll_no": "DL-2026-8492",
    "exam_title": "Deep Learning & Computer Vision Assessment",
    "exam_code": "CV-402",
    "duration_minutes": 15
}

# Structured Question Bank
EXAM_QUESTIONS = [
    {
        "id": "q1",
        "category": "Computer Vision",
        "marks": 1,
        "question": "Which framework is primarily used in this proctoring system for extracting 468 3D facial landmarks in real-time?",
        "options": [
            {"val": "mediapipe", "text": "MediaPipe Face Mesh"},
            {"val": "haar", "text": "Haar Cascade Classifiers"},
            {"val": "yolo", "text": "YOLOv3 Object Detection"},
            {"val": "resnet", "text": "Vanilla ResNet-18"}
        ],
        "answer": "mediapipe",
        "explanation": "MediaPipe Face Mesh predicts 468 3D facial landmarks using lightweight neural network models tailored for real-time inference."
    },
    {
        "id": "q2",
        "category": "Head Pose Estimation",
        "marks": 1,
        "question": "Which OpenCV function estimates the 3D rotation and translation vectors of a face by solving the Perspective-n-Point problem?",
        "options": [
            {"val": "cv2.solvePnP", "text": "cv2.solvePnP()"},
            {"val": "cv2.findHomography", "text": "cv2.findHomography()"},
            {"val": "cv2.warpAffine", "text": "cv2.warpAffine()"},
            {"val": "cv2.matchTemplate", "text": "cv2.matchTemplate()"}
        ],
        "answer": "cv2.solvePnP",
        "explanation": "cv2.solvePnP estimates object pose from 3D-to-2D point correspondences given camera intrinsic parameters."
    },
    {
        "id": "q3",
        "category": "Face Geometry",
        "marks": 1,
        "question": "In 3D head pose estimation, which three angular rotations represent orientation (nodding, turning side-to-side, and tilting)?",
        "options": [
            {"val": "pitch_yaw_roll", "text": "Pitch, Yaw, and Roll"},
            {"val": "rgb_channels", "text": "Red, Green, and Blue"},
            {"val": "alpha_beta_gamma", "text": "Alpha, Beta, and Gamma Rays"},
            {"val": "lat_long_alt", "text": "Latitude, Longitude, and Altitude"}
        ],
        "answer": "pitch_yaw_roll",
        "explanation": "Pitch represents up/down tilt, Yaw represents left/right rotation, and Roll represents tilting towards shoulders."
    },
    {
        "id": "q4",
        "category": "Integrity Monitoring",
        "marks": 1,
        "question": "What primary violation is flagged when the face detector registers more than one face simultaneously inside the camera stream?",
        "options": [
            {"val": "multiple_person", "text": "Multiple Faces / Third-Party Assistance Detected"},
            {"val": "lighting_error", "text": "Ambient Lighting Exposure Shift"},
            {"val": "compression_loss", "text": "Video Codec Compression Loss"},
            {"val": "audio_jitter", "text": "Microphone Frequency Jitter"}
        ],
        "answer": "multiple_person",
        "explanation": "Presence of multiple faces indicates potential external assistance or unauthorized bystanders in the examination area."
    },
    {
        "id": "q5",
        "category": "Image Preprocessing",
        "marks": 1,
        "question": "Which color space conversion must be executed on OpenCV BGR webcam frames before processing with MediaPipe?",
        "options": [
            {"val": "rgb", "text": "cv2.COLOR_BGR2RGB (RGB Color Space)"},
            {"val": "gray", "text": "cv2.COLOR_BGR2GRAY (Monochrome Grayscale)"},
            {"val": "hsv", "text": "cv2.COLOR_BGR2HSV (Hue Saturation Value)"},
            {"val": "lab", "text": "cv2.COLOR_BGR2LAB (Perceptually Uniform LAB)"}
        ],
        "answer": "rgb",
        "explanation": "OpenCV decodes frames in BGR format, whereas MediaPipe models expect inputs formatted in the RGB color space."
    }
]

# Mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                 max_num_faces=2,
                                 refine_landmarks=True,
                                 min_detection_confidence=0.5,
                                 min_tracking_confidence=0.5)

# Globals (prototype)
fault_count = 0
MAX_FAULTS = 10
violations = []

def save_violation(frame, reason):
    """Saves a violation image to static/evidence and records reason with timestamp."""
    global violations
    timestamp = datetime.now()
    filename = f"violation_{timestamp.strftime('%Y%m%d_%H%M%S_%f')}.jpg"
    filepath = os.path.join(EVIDENCE_DIR, filename)
    try:
        cv2.imwrite(filepath, frame)
        rel_path = os.path.join('static', 'evidence', filename).replace('\\', '/')
        violations.append({
            "file": rel_path,
            "filename": filename,
            "reason": reason,
            "timestamp": timestamp.strftime('%H:%M:%S'),
            "date": timestamp.strftime('%b %d, %Y')
        })
    except Exception as e:
        print("Failed to save violation image:", e)

def get_head_pose(landmarks, frame_w, frame_h):
    """Estimate head pose (pitch, yaw, roll) using selected landmarks."""
    face_2d, face_3d = [], []
    landmark_ids = [33, 263, 1, 61, 291, 199]
    for idx, lm in enumerate(landmarks.landmark):
        if idx in landmark_ids:
            x, y = int(lm.x * frame_w), int(lm.y * frame_h)
            face_2d.append([x, y])
            face_3d.append([x, y, lm.z * 3000])  # scale z to make solvePnP stable

    face_2d = np.array(face_2d, dtype=np.float64)
    face_3d = np.array(face_3d, dtype=np.float64)

    # Camera internals
    focal_length = frame_w
    cam_matrix = np.array([[focal_length, 0, frame_w / 2],
                           [0, focal_length, frame_h / 2],
                           [0, 0, 1]], dtype=np.float64)
    dist_matrix = np.zeros((4, 1), dtype=np.float64)

    # SolvePnP
    try:
        success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix, flags=cv2.SOLVEPNP_ITERATIVE)
        rmat, _ = cv2.Rodrigues(rot_vec)
        angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
        pitch, yaw, roll = angles[0], angles[1], angles[2]
        return pitch, yaw, roll
    except Exception as e:
        return 0.0, 0.0, 0.0

def analyze_frame(image_bgr):
    """Analyze a single BGR frame. Returns dict with status, severity, and faults."""
    global fault_count, violations
    frame_h, frame_w = image_bgr.shape[:2]
    rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    status = "Face OK"
    severity = "ok"

    if results.multi_face_landmarks:
        if len(results.multi_face_landmarks) > 1:
            status = "Multiple faces detected"
            severity = "danger"
            fault_count += 1
            save_violation(image_bgr, status)
        else:
            # single face: check head pose
            for face_landmarks in results.multi_face_landmarks:
                pitch, yaw, roll = get_head_pose(face_landmarks, frame_w, frame_h)
                # thresholds (tweakable)
                if yaw > 20:
                    status = "Look into camera (Right)"
                    severity = "warning"
                    fault_count += 1
                    save_violation(image_bgr, status)
                elif yaw < -20:
                    status = "Look into camera (Left)"
                    severity = "warning"
                    fault_count += 1
                    save_violation(image_bgr, status)
                elif pitch > 15:
                    status = "Look into camera (Down)"
                    severity = "warning"
                    fault_count += 1
                    save_violation(image_bgr, status)
                elif pitch < -15:
                    status = "Look into camera (Up)"
                    severity = "warning"
                    fault_count += 1
                    save_violation(image_bgr, status)
                else:
                    status = "Face OK"
                    severity = "ok"
    else:
        status = "Face not detected"
        severity = "danger"
        fault_count += 1
        save_violation(image_bgr, status)

    return {
        "status": status,
        "severity": severity,
        "faults": fault_count,
        "max_faults": MAX_FAULTS,
        "last_violation": violations[-1] if violations else None
    }

@app.route('/')
def index():
    global fault_count, violations
    # Initialize fresh session start if reset or first visit
    if 'exam_started' not in session:
        fault_count = 0
        violations = []
        session['exam_started'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return render_template(
        'exam.html',
        questions=EXAM_QUESTIONS,
        candidate=CANDIDATE_INFO,
        max_faults=MAX_FAULTS,
        total_questions=len(EXAM_QUESTIONS)
    )

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    """Resets proctoring metrics and starts a brand new assessment session."""
    global fault_count, violations
    fault_count = 0
    violations = []
    session.clear()
    session['exam_started'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return redirect(url_for('index'))

@app.route('/monitor', methods=['POST'])
def monitor():
    """Receives base64 frame, analyzes it and returns JSON result."""
    try:
        data = request.json.get('frame', None)
        if not data:
            return jsonify({"error": "no frame data"}), 400

        # Decode base64 image
        header, encoded = data.split(',', 1)
        img_data = base64.b64decode(encoded)
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        result = analyze_frame(frame)
        result['submit'] = True if result['faults'] >= MAX_FAULTS else False
        return jsonify(result)
    except Exception as e:
        print('Error in /monitor:', e)
        return jsonify({"error": str(e)}), 500

@app.route('/submit', methods=['POST'])
def submit():
    """Handles exam submission form, computes score, assesses integrity, and redirects to report."""
    global violations
    score = 0
    total = len(EXAM_QUESTIONS)
    answers_review = []

    for q in EXAM_QUESTIONS:
        qid = q['id']
        user_ans = request.form.get(qid)
        correct_ans = q['answer']
        # Backwards compatible check for legacy 2-question submissions:
        is_correct = (user_ans == correct_ans) or (qid == 'q1' and user_ans == '4') or (qid == 'q2' and user_ans == 'Delhi')

        if is_correct:
            score += 1

        selected_label = "Unanswered"
        for opt in q['options']:
            if opt['val'] == user_ans:
                selected_label = opt['text']
                break

        correct_label = ""
        for opt in q['options']:
            if opt['val'] == correct_ans:
                correct_label = opt['text']
                break

        answers_review.append({
            "id": qid,
            "category": q.get('category', 'General'),
            "question": q['question'],
            "user_ans": user_ans,
            "selected_label": selected_label,
            "correct_ans": correct_ans,
            "correct_label": correct_label,
            "is_correct": is_correct,
            "explanation": q.get('explanation', '')
        })

    # Calculate integrity index based on proctoring faults (100% minus 10% per violation)
    total_violations = len(violations)
    integrity_score = max(0, 100 - (total_violations * 10))

    if total_violations == 0:
        integrity_rating = "Excellent (Clean Record)"
        integrity_badge = "success"
    elif total_violations <= 3:
        integrity_rating = "Good (Minor Discrepancies)"
        integrity_badge = "info"
    elif total_violations <= 6:
        integrity_rating = "Moderate (Suspicious Activity)"
        integrity_badge = "warning"
    else:
        integrity_rating = "Critical (High Risk Flags)"
        integrity_badge = "danger"

    percentage = round((score / total) * 100, 1) if total > 0 else 0
    passed = percentage >= 50.0 and total_violations < MAX_FAULTS

    # Store full results in session
    session['score'] = score
    session['total_questions'] = total
    session['percentage'] = percentage
    session['passed'] = passed
    session['violations'] = violations
    session['total_violations'] = total_violations
    session['integrity_score'] = integrity_score
    session['integrity_rating'] = integrity_rating
    session['integrity_badge'] = integrity_badge
    session['answers_review'] = answers_review
    session['submitted_at'] = datetime.now().strftime('%b %d, %Y - %I:%M %p')

    return redirect(url_for('report'))

@app.route('/report')
def report():
    """Renders the executive proctoring audit and examination report."""
    if 'score' not in session:
        # Fallback if accessed without submitting
        return redirect(url_for('index'))

    return render_template(
        'report.html',
        candidate=CANDIDATE_INFO,
        score=session.get('score', 0),
        total_questions=session.get('total_questions', len(EXAM_QUESTIONS)),
        percentage=session.get('percentage', 0),
        passed=session.get('passed', False),
        violations=session.get('violations', []),
        total_violations=session.get('total_violations', 0),
        integrity_score=session.get('integrity_score', 100),
        integrity_rating=session.get('integrity_rating', 'Excellent'),
        integrity_badge=session.get('integrity_badge', 'success'),
        answers_review=session.get('answers_review', []),
        submitted_at=session.get('submitted_at', datetime.now().strftime('%b %d, %Y - %I:%M %p')),
        max_faults=MAX_FAULTS
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
