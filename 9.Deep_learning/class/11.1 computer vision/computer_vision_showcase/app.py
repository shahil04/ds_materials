from __future__ import annotations

from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Lock
from time import monotonic

import cv2
import numpy as np
import streamlit as st
from PIL import Image


class VideoRecorder:
    frame_width = 640
    frame_height = 480
    frame_rate = 15
    max_frames = 450
    max_duration = 30
    frame_interval = 1 / frame_rate

    def __init__(self) -> None:
        self._lock = Lock()
        self._frames: list[bytes] = []
        self._recording = False
        self._last_frame_at = 0.0
        self._recording_started_at = 0.0
        self._limit_reached = False

    def set_recording(self, recording: bool) -> bool:
        with self._lock:
            started = recording and not self._recording
            if started:
                self._frames.clear()
                self._last_frame_at = 0.0
                self._recording_started_at = monotonic()
                self._limit_reached = False
            self._recording = recording
            return started

    def add_frame(self, frame: np.ndarray) -> None:
        with self._lock:
            if not self._recording:
                return
            timestamp = monotonic()
            if (
                len(self._frames) >= self.max_frames
                or timestamp - self._recording_started_at >= self.max_duration
            ):
                self._limit_reached = True
                return
            if timestamp - self._last_frame_at < self.frame_interval:
                return

            height, width = frame.shape[:2]
            scale = min(self.frame_width / width, self.frame_height / height)
            resized = cv2.resize(
                frame,
                (max(1, round(width * scale)), max(1, round(height * scale))),
            )
            canvas = np.zeros(
                (self.frame_height, self.frame_width, 3),
                dtype=np.uint8,
            )
            top = (self.frame_height - resized.shape[0]) // 2
            left = (self.frame_width - resized.shape[1]) // 2
            canvas[
                top : top + resized.shape[0],
                left : left + resized.shape[1],
            ] = resized
            success, encoded = cv2.imencode(
                ".jpg",
                canvas,
                [int(cv2.IMWRITE_JPEG_QUALITY), 80],
            )
            if not success:
                raise RuntimeError("Could not encode a webcam frame.")
            self._frames.append(encoded.tobytes())
            self._last_frame_at = timestamp
            self._limit_reached = len(self._frames) >= self.max_frames

    @property
    def frame_count(self) -> int:
        with self._lock:
            return len(self._frames)

    @property
    def limit_reached(self) -> bool:
        with self._lock:
            return self._limit_reached

    def to_mp4(self) -> bytes:
        with self._lock:
            frames = list(self._frames)
        if not frames:
            raise ValueError("No video frames have been recorded.")

        with TemporaryDirectory(prefix="computer-vision-camera-") as temp_dir:
            output_path = Path(temp_dir) / "camera-recording.mp4"
            writer = cv2.VideoWriter(
                str(output_path),
                cv2.VideoWriter_fourcc(*"mp4v"),
                self.frame_rate,
                (self.frame_width, self.frame_height),
            )
            if not writer.isOpened():
                raise RuntimeError("OpenCV could not create an MP4 video.")
            try:
                for encoded in frames:
                    frame = cv2.imdecode(
                        np.frombuffer(encoded, dtype=np.uint8),
                        cv2.IMREAD_COLOR,
                    )
                    if frame is None:
                        raise RuntimeError("A recorded webcam frame could not be decoded.")
                    writer.write(frame)
            finally:
                writer.release()
            if not output_path.is_file() or output_path.stat().st_size == 0:
                raise RuntimeError("The MP4 recording could not be finalized.")
            return output_path.read_bytes()

    def clear(self) -> None:
        with self._lock:
            self._frames.clear()
            self._recording = False
            self._last_frame_at = 0.0
            self._recording_started_at = 0.0
            self._limit_reached = False


def _upload_image(key: str) -> np.ndarray | None:
    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png", "bmp"],
        key=key,
    )
    if uploaded_file is None:
        st.info("Upload a JPG, PNG, or BMP image to try this demo.")
        return None

    try:
        return np.asarray(Image.open(uploaded_file).convert("RGB"))
    except (OSError, ValueError) as error:
        st.error(f"Could not open the uploaded image: {error}")
        return None


def _download_png(image: np.ndarray) -> bytes:
    buffer = BytesIO()
    Image.fromarray(image).save(buffer, format="PNG")
    return buffer.getvalue()


def _show_result(
    original: np.ndarray,
    processed: np.ndarray,
    result_caption: str,
    download_name: str,
) -> None:
    original_column, result_column = st.columns(2)
    original_column.image(
        original,
        caption="Original",
        alt="Uploaded source image",
        width="stretch",
    )
    result_column.image(
        processed,
        caption=result_caption,
        alt=result_caption,
        width="stretch",
    )
    st.download_button(
        "Download result",
        data=_download_png(processed),
        file_name=download_name,
        mime="image/png",
        key=f"download-{download_name}",
    )


def _render_image_filters() -> None:
    st.subheader("Image filters")
    st.caption("Try classic image processing operations from the OpenCV projects.")
    image = _upload_image("filters-image")
    if image is None:
        return

    operation = st.selectbox(
        "Choose a filter",
        [
            "Grayscale",
            "Gaussian blur",
            "Canny edges",
            "Binary threshold",
            "Cartoon effect",
            "Rotate",
        ],
        key="filter-operation",
    )
    if operation == "Gaussian blur":
        kernel_size = st.slider("Blur strength", 3, 21, 9, step=2)
    elif operation == "Canny edges":
        threshold = st.slider("Edge threshold", 20, 200, 80)
    elif operation == "Rotate":
        angle = st.slider("Rotation angle", -180, 180, 45)

    if operation == "Grayscale":
        processed = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    elif operation == "Gaussian blur":
        processed = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    elif operation == "Canny edges":
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        processed = cv2.Canny(gray, threshold, threshold * 2)
    elif operation == "Binary threshold":
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, processed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    elif operation == "Cartoon effect":
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        block_size = min(9, min(gray.shape))
        if block_size % 2 == 0:
            block_size -= 1
        if block_size < 3:
            st.error("Cartoon effect needs an image at least 3 pixels wide and tall.")
            return
        smooth = cv2.bilateralFilter(image, 9, 75, 75)
        mask = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            block_size,
            9,
        )
        processed = cv2.bitwise_and(smooth, smooth, mask=mask)
    else:
        height, width = image.shape[:2]
        matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
        processed = cv2.warpAffine(image, matrix, (width, height))

    _show_result(image, processed, operation, "image_filter_result.png")


def _render_face_detection() -> None:
    st.subheader("Face detection")
    st.caption("Detect faces in a photo using OpenCV's built-in Haar cascade.")
    image = _upload_image("face-image")
    if image is None:
        return

    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(cascade_path)
    if detector.empty():
        st.error(f"OpenCV could not load its face detector: {cascade_path}")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(24, 24),
    )
    annotated = image.copy()
    for x, y, width, height in faces:
        cv2.rectangle(annotated, (x, y), (x + width, y + height), (0, 220, 80), 3)
    st.metric("Faces detected", len(faces))
    _show_result(image, annotated, "Detected faces", "face_detection_result.png")


def _render_people_detection() -> None:
    st.subheader("People detection")
    st.caption("Find people with OpenCV's pre-trained HOG pedestrian detector.")
    image = _upload_image("people-image")
    if image is None:
        return
    if not st.button("Detect people", type="primary", key="detect-people"):
        st.image(image, caption="Uploaded image", alt="Image awaiting detection")
        return

    height, width = image.shape[:2]
    scale = min(1.0, 900 / max(height, width))
    resized = cv2.resize(
        image,
        (max(1, round(width * scale)), max(1, round(height * scale))),
    )
    detector = cv2.HOGDescriptor()
    detector.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    boxes, _weights = detector.detectMultiScale(
        cv2.cvtColor(resized, cv2.COLOR_RGB2BGR),
        hitThreshold=0,
        winStride=(8, 8),
        padding=(8, 8),
        scale=1.05,
    )

    annotated = image.copy()
    for x, y, box_width, box_height in boxes:
        x1 = round(x / scale)
        y1 = round(y / scale)
        x2 = round((x + box_width) / scale)
        y2 = round((y + box_height) / scale)
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 220, 80), 3)
    st.metric("People detected", len(boxes))
    _show_result(image, annotated, "Detected people", "people_detection_result.png")


def _render_qr_scanner() -> None:
    st.subheader("QR code scanner")
    st.caption("Decode and outline a QR code from an uploaded image.")
    image = _upload_image("qr-image")
    if image is None:
        return

    detector = cv2.QRCodeDetector()
    decoded, points, _straight = detector.detectAndDecode(
        cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    )
    annotated = image.copy()
    if points is not None:
        polygon = np.asarray(points, dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(annotated, [polygon], True, (0, 220, 80), 3)
    if decoded:
        st.success(f"QR content: {decoded}")
    else:
        st.info("No readable QR code was found in this image.")
    _show_result(image, annotated, "QR scan", "qr_scan_result.png")


def _order_corners(points: np.ndarray) -> np.ndarray:
    ordered = np.zeros((4, 2), dtype=np.float32)
    sums = points.sum(axis=1)
    differences = np.diff(points, axis=1)
    ordered[0] = points[np.argmin(sums)]
    ordered[2] = points[np.argmax(sums)]
    ordered[1] = points[np.argmin(differences)]
    ordered[3] = points[np.argmax(differences)]
    return ordered


def _scan_document(image: np.ndarray) -> np.ndarray | None:
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _hierarchy = cv2.findContours(
        edges,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    corners = None
    image_area = image.shape[0] * image.shape[1]
    for contour in contours[:20]:
        if cv2.contourArea(contour) < image_area * 0.1:
            break
        perimeter = cv2.arcLength(contour, True)
        polygon = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(polygon) == 4:
            corners = _order_corners(polygon.reshape(4, 2))
            break
    if corners is None:
        return None

    top_left, top_right, bottom_right, bottom_left = corners
    output_width = round(
        max(np.linalg.norm(bottom_right - bottom_left), np.linalg.norm(top_right - top_left))
    )
    output_height = round(
        max(np.linalg.norm(top_right - bottom_right), np.linalg.norm(top_left - bottom_left))
    )
    if output_width < 2 or output_height < 2:
        return None
    destination = np.array(
        [
            [0, 0],
            [output_width - 1, 0],
            [output_width - 1, output_height - 1],
            [0, output_height - 1],
        ],
        dtype=np.float32,
    )
    transform = cv2.getPerspectiveTransform(corners, destination)
    return cv2.warpPerspective(image, transform, (output_width, output_height))


def _render_document_scanner() -> None:
    st.subheader("Document scanner")
    st.caption("Find a page outline and correct its perspective.")
    image = _upload_image("document-image")
    if image is None:
        return

    scanned = _scan_document(image)
    if scanned is None:
        st.warning("No clear four-corner page was found. Try a photo with visible edges.")
        return
    _show_result(image, scanned, "Scanned document", "scanned_document.png")


def _render_contours() -> None:
    st.subheader("Shape and contour detection")
    st.caption("Threshold an image and outline the external shapes.")
    image = _upload_image("contour-image")
    if image is None:
        return

    threshold = st.slider("Threshold", 0, 255, 120, key="contour-threshold")
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _level, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    contours, _hierarchy = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    annotated = image.copy()
    cv2.drawContours(annotated, contours, -1, (0, 220, 80), 2)
    st.metric("Contours found", len(contours))
    _show_result(image, annotated, "Detected contours", "contour_result.png")


def _render_surface_inspection() -> None:
    st.subheader("Surface inspection")
    st.caption(
        "Highlight strong edge regions as a classic OpenCV defect-inspection demo. "
        "This is a visual aid, not a trained defect classifier."
    )
    image = _upload_image("surface-image")
    if image is None:
        return

    minimum_area = st.slider(
        "Ignore regions smaller than",
        5,
        500,
        40,
        key="surface-min-area",
    )
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 60, 160)
    kernel = np.ones((3, 3), dtype=np.uint8)
    connected = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    contours, _hierarchy = cv2.findContours(
        connected,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    regions = [contour for contour in contours if cv2.contourArea(contour) >= minimum_area]
    annotated = image.copy()
    cv2.drawContours(annotated, regions, -1, (255, 40, 40), 2)
    st.metric("Regions highlighted", len(regions))
    _show_result(image, annotated, "Highlighted regions", "surface_inspection.png")


def _render_hand_landmarks() -> None:
    st.subheader("Hand landmarks")
    st.caption("Track hand landmarks with the MediaPipe Hands model.")
    image = _upload_image("hand-image")
    if image is None:
        return
    if not st.button("Detect hand landmarks", type="primary", key="detect-hands"):
        st.image(image, caption="Uploaded image", alt="Image awaiting hand detection")
        return

    try:
        import mediapipe as mp

        hands_module = mp.solutions.hands
        with hands_module.Hands(
            static_image_mode=True,
            max_num_hands=2,
            min_detection_confidence=0.5,
        ) as detector:
            results = detector.process(image)
        annotated = image.copy()
        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    annotated,
                    landmarks,
                    hands_module.HAND_CONNECTIONS,
                )
            st.success(f"Hands detected: {len(results.multi_hand_landmarks)}")
        else:
            st.info("No hands were found in this image.")
        _show_result(image, annotated, "Hand landmarks", "hand_landmarks.png")
    except (ImportError, AttributeError, OSError, RuntimeError) as error:
        st.error(f"MediaPipe could not run the hand-landmark demo: {error}")


def _render_ocr() -> None:
    st.subheader("Text recognition")
    st.caption("Read printed text from an image with Tesseract OCR.")
    image = _upload_image("ocr-image")
    if image is None:
        return
    if not st.button("Read text", type="primary", key="run-ocr"):
        st.image(image, caption="Uploaded image", alt="Image awaiting text recognition")
        return

    try:
        import pytesseract
        from pytesseract import Output

        data = pytesseract.image_to_data(
            image,
            output_type=Output.DICT,
            config="--psm 6",
        )
    except ImportError as error:
        st.error(f"OCR requires pytesseract: {error}")
        return
    except (OSError, RuntimeError) as error:
        st.error(f"Tesseract OCR could not run: {error}")
        return
    except pytesseract.TesseractError as error:
        st.error(f"Tesseract OCR reported an error: {error}")
        return

    recognized_words = []
    annotated = image.copy()
    for index, word in enumerate(data["text"]):
        word = word.strip()
        try:
            confidence = float(data["conf"][index])
        except (ValueError, TypeError):
            continue
        if not word or confidence < 0:
            continue
        recognized_words.append(word)
        x = int(data["left"][index])
        y = int(data["top"][index])
        width = int(data["width"][index])
        height = int(data["height"][index])
        cv2.rectangle(annotated, (x, y), (x + width, y + height), (0, 220, 80), 2)

    text = " ".join(recognized_words)
    if text:
        st.text_area("Recognized text", text, height=140)
    else:
        st.info("No text was recognized.")
    _show_result(image, annotated, "OCR word regions", "ocr_result.png")


def _render_camera() -> None:
    st.subheader("Camera capture")
    st.caption(
        "Take a still photo or start a live webcam session to record a short video. "
        "Allow camera access when your browser asks. If blocked, enable camera "
        "permission for this localhost site in the browser settings."
    )
    capture_mode = st.segmented_control(
        "Capture mode",
        ["Photo", "Live video"],
        default="Photo",
        key="camera-capture-mode",
    )
    if capture_mode == "Photo":
        photo = st.camera_input("Take a photo", key="camera-photo")
        if photo is not None:
            try:
                image = np.asarray(Image.open(photo).convert("RGB"))
            except (OSError, ValueError) as error:
                st.error(f"Could not open the captured photo: {error}")
                return
            st.image(
                image,
                caption="Captured photo",
                alt="Photo captured with the webcam",
                width="stretch",
            )
            st.download_button(
                "Download photo",
                data=photo.getvalue(),
                file_name="camera_photo.jpg",
                mime="image/jpeg",
                key="download-camera-photo",
            )
        return

    try:
        from streamlit_webrtc import webrtc_streamer
    except ImportError as error:
        st.error(f"Live video requires streamlit-webrtc: {error}")
        return

    if "camera_video_recorder" not in st.session_state:
        st.session_state["camera_video_recorder"] = VideoRecorder()
    recorder = st.session_state["camera_video_recorder"]

    def capture_frame(frame):
        recorder.add_frame(frame.to_ndarray(format="bgr24"))
        return frame

    context = webrtc_streamer(
        key="computer-vision-live-camera",
        video_frame_callback=capture_frame,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )
    if context.state.playing:
        recording = st.toggle("Record video", key="record-camera-video")
        if recorder.set_recording(recording):
            st.session_state.pop("camera_video_download", None)
    else:
        recorder.set_recording(False)
        st.info("Select START on the live video panel and allow camera access.")

    st.caption(
        "Video is limited to 30 seconds and kept only in this Streamlit session."
    )
    if recorder.limit_reached:
        st.warning("The 30-second recording limit was reached. Stop recording to download it.")
    if recorder.frame_count:
        st.write(f"Recorded frames: {recorder.frame_count}")
    if recorder.frame_count and context.state.playing and not recording:
        st.info("Turn off recording, then select STOP to prepare the video download.")
    if recorder.frame_count and not context.state.playing:
        if st.button("Prepare video download", key="prepare-camera-video"):
            try:
                st.session_state["camera_video_download"] = recorder.to_mp4()
            except (OSError, RuntimeError, ValueError) as error:
                st.error(f"Could not prepare the video: {error}")
        video = st.session_state.get("camera_video_download")
        if video:
            st.download_button(
                "Download video",
                data=video,
                file_name="camera_recording.mp4",
                mime="video/mp4",
                key="download-camera-video",
            )
        if st.button("Discard recording", key="discard-camera-video"):
            recorder.clear()
            st.session_state.pop("camera_video_download", None)
            st.rerun()


def main() -> None:
    st.set_page_config(
        page_title="Computer vision demos",
        page_icon=":material/photo_camera:",
        layout="wide",
    )
    st.title("Computer vision demos")
    st.write(
        "Choose a demo, upload an image, and see the computer-vision result. "
        "No project folders or source listings are shown here."
    )

    demo_labels = [
        "Image filters",
        "Face detection",
        "People detection",
        "QR scanner",
        "Document scanner",
        "Contours",
        "Surface inspection",
        "Hand landmarks",
        "Text recognition",
        "Camera",
    ]
    demo_tabs = st.tabs(demo_labels, on_change="rerun")
    renderers = [
        _render_image_filters,
        _render_face_detection,
        _render_people_detection,
        _render_qr_scanner,
        _render_document_scanner,
        _render_contours,
        _render_surface_inspection,
        _render_hand_landmarks,
        _render_ocr,
        _render_camera,
    ]
    for label, tab, render in zip(demo_labels, demo_tabs, renderers):
        if tab.open:
            with tab:
                render()


if __name__ == "__main__":
    main()
