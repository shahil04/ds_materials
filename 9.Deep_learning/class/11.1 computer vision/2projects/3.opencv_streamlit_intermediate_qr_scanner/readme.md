# OpenCV Computer Vision Projects

A comprehensive collection of hands-on **Computer Vision** mini-projects and utilities built using Python and OpenCV. This repository showcases various practical applications ranging from core image processing techniques to advanced object tracking and real-time detection tasks.

## 🚀 Projects Overview

The repository consists of the following core modules:

* **basic_ops.py**: Fundamental pixel manipulations, image transformations, and cropping operations.
* **cartoonify.py**: Transforms real-world photographs into stylized cartoon drawings using bilateral filters and edge detection techniques.
* **color_detection.py**: Isolates, masks, and identifies specific color spaces and objects within a live camera stream or image.
* **document_scanner.py**: Automatic edge detection, perspective warping, and thresholding to scan physical documents cleanly.
* **face_detection.py**: Localizes human faces in images or real-time video using pre-trained Haar Cascades or deep learning models.
* **filters.py**: Custom image filters, including blurs, sharpening masks, color tints, and artistic adjustments.
* **hand_gesture.py**: Recognizes and tracks hand keypoints to translate real-time movements into interactive system commands.
* **image_stitching.py**: Combines multiple overlapping images into a single, seamless panoramic view.
* **motion_tracking.py**: Background subtraction and contour analysis to detect, highlight, and monitor moving elements over time.
* **object_measurement.py**: Computes the real-world dimensions (width and height) of target objects using a pixel-to-metric ratio from a reference item.
* **qr_barcode_scanner.py**: Scans, decodes, and highlights barcodes and QR codes dynamically from a video stream.
* **shapes.py**: Detects contours, matches geometries, and labels basic geometric shapes like triangles, squares, and circles.

## 🛠️ Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com
   cd opencv-computer-vision-projects
   ```

2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install opencv-python numpy pyzbar mediapipe
   ```

## 💻 Usage

Run any project module directly from your terminal using Python. For example, to launch the motion tracking script:

```bash
python motion_tracking.py
```

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
