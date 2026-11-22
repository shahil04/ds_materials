from flask import Flask, render_template, request, jsonify, redirect, url_for
import cv2
import mediapipe as mp
import numpy as np
import os
import base64
from datetime import datetime

app = Flask(__name__)
app.config['EVIDENCE_DIR'] = 'static/evidence'

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

violations = {}
MAX_VIOLATIONS = 10

def save_evidence(image_data, reason, student_id='default'):
    if not os.path.exists(app.config['EVIDENCE_DIR']):
        os.makedirs(app.config['EVIDENCE_DIR'])
    filename = f"{student_id}_{reason}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = os.path.join(app.config['EVIDENCE_DIR'], filename)
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(image_data.split(',')[1]))
    return filename

@app.route('/')
def index():
    return redirect(url_for('exam'))

@app.route('/exam')
def exam():
    return render_template('exam.html')

@app.route('/monitor', methods=['POST'])
def monitor():
    global violations
    student_id = 'default'

    data = request.json
    image_data = data['image']
    np_img = np.frombuffer(base64.b64decode(image_data.split(',')[1]), np.uint8)
    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        message = None
        if not results.detections:
            message = "Face not detected!"
        elif len(results.detections) > 1:
            message = "Multiple faces detected!"
        else:
            h, w, _ = frame.shape
            bbox = results.detections[0].location_data.relative_bounding_box
            x, y, box_w, box_h = int(bbox.xmin * w), int(bbox.ymin * h), int(bbox.width * w), int(bbox.height * h)
            cx, cy = x + box_w // 2, y + box_h // 2
            if cx < w*0.3:
                message = "Please look right"
            elif cx > w*0.7:
                message = "Please look left"
            elif cy < h*0.3:
                message = "Please look down"
            elif cy > h*0.7:
                message = "Please look up"

        if message:
            violations.setdefault(student_id, [])
            if len(violations[student_id]) < MAX_VIOLATIONS:
                filename = save_evidence(image_data, message, student_id)
                violations[student_id].append((message, filename))

        if len(violations.get(student_id, [])) >= MAX_VIOLATIONS:
            return jsonify({'status': 'submit', 'message': 'Too many violations! Submitting exam.'})

        return jsonify({'status': 'ok', 'message': message})

@app.route('/submit_exam', methods=['POST'])
def submit_exam():
    student_id = 'default'
    student_violations = violations.get(student_id, [])
    return render_template('report.html', violations=student_violations)

if __name__ == '__main__':
    app.run(debug=True)
