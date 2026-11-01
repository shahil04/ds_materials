PROCTOR-AI : Face-Proctored Online Assessment System
======================================================

An attractive, enterprise-grade proctored online examination interface powered by Flask, OpenCV, and MediaPipe Face Mesh.

Key Features:
-------------
1. Modern Online Assessment UI:
   - Fixed Exam Header with Candidate Profile, Exam Code, and Live 15-Minute Countdown Timer.
   - Dynamic Question Navigator Palette (Answered, Not Visited, Marked for Review, Current Question).
   - Interactive Option Cards with smooth hover effects, keyboard & click selection, and completion progress bar.

2. AI Video Proctoring HUD:
   - Live Webcam Feed with futuristic cyber-corner reticles and animated scanning laser.
   - Real-time status badge:
       * 🟢 Face Verified & Active
       * 🟡 Warning: Head Pose Deviations (Looking Left, Right, Up, or Down)
       * 🔴 Violation: Multiple Faces Detected / Face Absent
   - Real-time Violation Progress Bar (0 / 10 Faults threshold).
   - Audio warning chimes on integrity infractions (Web Audio API synth).
   - Auto-submission safeguards when maximum fault threshold (10 faults) is exceeded.
   - Tab-switching & Window Blur monitoring (alerts candidates if they leave the exam tab).

3. Executive Audit & Verification Report:
   - Official certification report with Score Gauge, Percentage, and Pass/Fail status.
   - 4 Core KPI Metrics: Proctor Integrity Index (0-100%), Violations Count, Questions Correct, and AI Verdict.
   - Captured Evidence Gallery: Grid of violation snapshots with timestamps and violation tags.
   - Fullscreen Lightbox Modal to inspect evidence images.
   - Detailed Answer Key Breakdown with conceptual explanations.
   - Print-ready stylesheet for 1-click PDF download (`window.print()`).

How to Run:
-----------
1. Activate your Python environment (Python 3.10 recommended):
   conda activate cvenv
   # or
   venv\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Start the Flask application:
   python app.py

4. Open your browser:
   http://localhost:5000

   * Allow camera permissions when prompted by your browser.
   * Click "Start Assessment Now" to initialize the proctoring camera.
