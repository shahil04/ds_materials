# 🛡️ PROCTOR-AI : Face-Proctored Online Assessment System

An attractive, enterprise-grade online examination assessment portal with real-time AI computer vision proctoring built using **Flask**, **OpenCV**, and **MediaPipe Face Mesh**.

---

## ⚡ Quick Start with Conda (`cvenv`)

### 1. Open Terminal / Anaconda Prompt
Navigate to the project directory:
```bash
cd "c:\Users\hp\Documents\ds_materials\9.Deep_learning\class\11.1 computer vision\2projects\5.flask_face_exam_complete\flask_face_exam_complete"
```

### 2. Activate Conda Environment
```bash
conda activate cvenv
```

> **Note:** The `cvenv` environment is already configured with Python 3.10, Flask, OpenCV (`opencv-python`), MediaPipe, and NumPy.

### 3. Run the Application
```bash
python app.py
```

### 4. Access the Exam Portal
Open your web browser (Chrome, Edge, or Firefox) and visit:
👉 **[http://localhost:5000](http://localhost:5000)**

---

## 🎯 Key Interface Features

### 🖥️ Examination Workspace
- **Dynamic 15-Minute Timer**: Digital countdown timer with automated warnings at 5 minutes, 2 minutes, and auto-submit on 00:00.
- **Candidate Profile Pill**: Candidate details, exam ID, and verified status.
- **Progress Tracker**: Real-time progress bar updating as questions are answered.
- **Interactive Option Cards**: Custom option pills (A, B, C, D) with hover animations and glowing selection borders.
- **Action Toolbar**: `Previous Question`, `Clear Selection`, `Mark for Review`, and `Save & Next`.

### 👁️ AI Proctoring HUD
- **Targeting Reticle & Animated Scanline**: Real-time cyber HUD overlay on top of the webcam feed.
- **Live Facial Orientation & Head Pose Tracking**:
  - 🟢 **`Face Verified`**: Head oriented towards the screen within safe thresholds.
  - 🟡 **`Look into camera (Left / Right / Up / Down)`**: Detected yaw or pitch head turn.
  - 🔴 **`Multiple faces detected`**: Flagged when more than one person enters the frame.
  - 🔴 **`Face not detected`**: Flagged if candidate leaves the camera view.
- **Real-Time Fault Counter Bar**: Live indicator tracking infractions towards the 10-fault maximum.
- **Web Audio Synth Alerts**: Subtle audio warning beeps on detected integrity infractions.
- **Tab-Switching & Window Blur Monitor**: Detects if candidate switches browser tabs or minimizes window.

### 📋 Interactive Question Palette
- **5-Question Quick Jump Grid**:
  - 🟢 **Green**: Answered
  - ⚪ **White**: Not Visited
  - 🟣 **Purple**: Marked for Review
  - 🟡 **Ring Outline**: Current Question

### 📊 Official Audit & Certification Report
- **Performance Overview**: Overall score gauge, percentage, and PASSED / NEEDS REVIEW status badge.
- **4 Core Integrity KPIs**:
  - Proctoring Integrity Index (0–100%)
  - Violation Snapshots Count
  - Total Questions Correct
  - Final AI Proctor Verdict
- **Captured Evidence Gallery**: Visual grid of all violation frames with timestamps and infraction reasons. Click any snapshot to inspect in the fullscreen Lightbox modal.
- **Conceptual Answer Explanations**: In-depth explanation for every question.
- **Print to PDF**: Built-in `@media print` styling for 1-click official certificate printing.

---

## 📁 Project Structure

```plaintext
flask_face_exam_complete/
│
├── app.py                     # Flask backend, MediaPipe face mesh & solvePnP head pose analysis
├── cvenv_requirements.txt     # Complete environment package list
├── requirements.txt           # Core project dependencies
├── readme.md                  # Project documentation & run guide
│
├── templates/
│   ├── exam.html              # Proctored online assessment interface
│   └── report.html            # Official examination & proctoring audit report
│
└── static/
    ├── css/
    │   ├── exam.css           # Styling for exam portal, HUD reticles, and modals
    │   └── report.css         # Styling for verification report and evidence lightbox
    ├── js/
    │   └── camera.js          # Webcam capture loop, AI status updates, audio alerts, and navigation
    └── evidence/              # Automatically stored JPEG violation snapshot frames
```

---

## ⚙️ Tech Stack
- **Backend Framework**: Python Flask
- **Computer Vision**: OpenCV (`cv2.solvePnP`, `cv2.Rodrigues`, `cv2.RQDecomp3x3`)
- **Facial Landmark Mesh**: MediaPipe FaceMesh (468 3D landmarks)
- **Frontend Engine**: HTML5, Vanilla JavaScript, CSS3 Design System, Web Audio API

