# Computer vision demos

The app is a single-file Streamlit frontend with interactive computer-vision
demos. It presents image filters, face and people detection, QR scanning,
document scanning, contour detection, surface inspection, MediaPipe hand
landmarks, OCR, and photo/video camera capture as feature tabs—not as a
project-folder browser.

## Run

From the `11.1 computer vision` folder, run:

```powershell
& ".\.venv\Scripts\python.exe" -m streamlit run ".\computer_vision_showcase\app.py"
```

Or install the packages in `requirements.txt` in your Python environment and
run `streamlit run app.py` from this folder.

## What's included

- `app.py`: all demo UI and image-processing code in one Python file.
- `source_code\`: copies of the Python files, preserving their original folder
  structure for reference; these files are not shown in the demo frontend.
- `requirements.txt`: Python packages used by the demos.

The hand-landmark and OCR demos also need MediaPipe and pytesseract. OCR needs
the Tesseract executable installed separately. The live video demo uses
streamlit-webrtc and records up to 30 seconds; allow camera access in the
browser. Camera capture works on localhost or another secure (HTTPS) origin.
Video is kept in the current Streamlit session until downloaded or discarded.
Original project files remain in place.
