import io
import re
import shutil
from pathlib import Path

import cv2
import fitz
import numpy as np
import pytesseract
import streamlit as st
from PIL import Image, UnidentifiedImageError
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(page_title="OCR Studio", page_icon="🔎", layout="wide")


def configure_tesseract():
    executable = shutil.which("tesseract")
    if executable is None:
        for candidate in (
            Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
            Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
        ):
            if candidate.is_file():
                executable = str(candidate)
                break

    if executable is not None:
        pytesseract.pytesseract.tesseract_cmd = executable


def load_cv_image(image_bytes):
    encoded = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("The uploaded file could not be decoded as an image.")
    return image


def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 3)
    _, thresholded = cv2.threshold(
        blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return thresholded


def extract_pdf_text(pdf_bytes):
    extracted_pages = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
        for page in document:
            page_text = page.get_text().strip()
            if page_text:
                extracted_pages.append(page_text)
            else:
                pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                page_image = Image.frombytes(
                    "RGB", (pixmap.width, pixmap.height), pixmap.samples
                )
                extracted_pages.append(pytesseract.image_to_string(page_image))
    return "\n".join(extracted_pages).strip()


def extract_uploaded_text(uploaded_file, is_resume):
    suffix = Path(uploaded_file.name).suffix.lower()
    content = uploaded_file.getvalue()

    if suffix == ".pdf":
        return extract_pdf_text(content)
    if suffix == ".txt":
        return content.decode("utf-8-sig", errors="replace").strip()
    if is_resume and suffix in {".png", ".jpg", ".jpeg"}:
        with Image.open(io.BytesIO(content)) as image:
            return pytesseract.image_to_string(image).strip()
    raise ValueError(f"Unsupported file type: {suffix or 'unknown'}")


def find_number_plate(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, 11, 17, 17)
    edges = cv2.Canny(blurred, 10, 200)
    contours, _ = cv2.findContours(
        edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    image_area = image.shape[0] * image.shape[1]
    candidates = []
    for contour in sorted(contours, key=cv2.contourArea, reverse=True)[:30]:
        perimeter = cv2.arcLength(contour, True)
        approximation = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approximation) != 4:
            continue

        x, y, width, height = cv2.boundingRect(approximation)
        aspect_ratio = width / max(height, 1)
        area_ratio = (width * height) / max(image_area, 1)
        if 2 <= aspect_ratio <= 6 and area_ratio >= 0.003:
            candidates.append((width * height, x, y, width, height))

    if not candidates:
        return None, None

    _, x, y, width, height = max(candidates)
    plate_crop = gray[y : y + height, x : x + width]
    annotated = image.copy()
    cv2.rectangle(annotated, (x, y), (x + width, y + height), (0, 255, 0), 3)
    return plate_crop, annotated


def calculate_ats_match(resume_text, job_text):
    vectorizer = CountVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_text])
    similarity = float(cosine_similarity(vectors[0], vectors[1])[0][0])

    feature_names = vectorizer.get_feature_names_out()
    resume_terms = vectors[0].toarray()[0] > 0
    job_terms = vectors[1].toarray()[0] > 0
    missing_terms = [
        term
        for term, in_resume, in_job in zip(feature_names, resume_terms, job_terms)
        if in_job and not in_resume
    ]
    return round(similarity * 100, 1), missing_terms


configure_tesseract()

st.title("OCR Studio")
st.caption("Image processing, text extraction, number-plate OCR, and resume matching.")

gray_tab, text_tab, plate_tab, ats_tab = st.tabs(
    [
        "1. Image to Gray",
        "2. Image to Text",
        "3. Number Plate",
        "4. Resume ATS",
    ]
)

with gray_tab:
    st.subheader("Convert an image to grayscale")
    gray_upload = st.file_uploader(
        "Choose an image", type=["png", "jpg", "jpeg"], key="gray_image"
    )
    if gray_upload is not None:
        try:
            image = load_cv_image(gray_upload.getvalue())
            grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            original_col, gray_col = st.columns(2)
            original_col.image(
                cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
                caption="Original image",
                use_container_width=True,
            )
            gray_col.image(
                grayscale,
                caption="Grayscale image",
                channels="GRAY",
                use_container_width=True,
            )
            st.download_button(
                "Download grayscale image",
                data=cv2.imencode(".png", grayscale)[1].tobytes(),
                file_name="grayscale.png",
                mime="image/png",
                key="download_gray",
            )
        except ValueError as error:
            st.error(str(error))

with text_tab:
    st.subheader("Extract text from an image")
    text_upload = st.file_uploader(
        "Choose an image with text", type=["png", "jpg", "jpeg"], key="text_image"
    )
    if text_upload is not None:
        try:
            image = load_cv_image(text_upload.getvalue())
            original_col, processed_col = st.columns(2)
            original_col.image(
                cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
                caption="Original image",
                use_container_width=True,
            )
            processed = preprocess_image(image)
            processed_col.image(
                processed,
                caption="Preprocessed image",
                channels="GRAY",
                use_container_width=True,
            )
            if st.button("Extract text", key="extract_image_text"):
                with st.spinner("Running OCR..."):
                    extracted_text = pytesseract.image_to_string(
                        processed, config="--psm 6"
                    ).strip()
                if extracted_text:
                    st.text_area("Extracted text", extracted_text, height=220)
                    st.download_button(
                        "Download extracted text",
                        data=extracted_text,
                        file_name="extracted_text.txt",
                        mime="text/plain",
                        key="download_extracted_text",
                    )
                else:
                    st.info("No text was detected in this image.")
        except ValueError as error:
            st.error(str(error))
        except pytesseract.TesseractNotFoundError:
            st.error(
                "Tesseract OCR was not found. Install the Tesseract OCR engine "
                "and add its executable to PATH."
            )
        except pytesseract.TesseractError as error:
            st.error(f"Tesseract could not process this image: {error}")

with plate_tab:
    st.subheader("Detect and read a vehicle number plate")
    plate_upload = st.file_uploader(
        "Choose a vehicle image", type=["png", "jpg", "jpeg"], key="plate_image"
    )
    if plate_upload is not None:
        try:
            image = load_cv_image(plate_upload.getvalue())
            if st.button("Find number plate", key="find_plate"):
                plate_crop, annotated = find_number_plate(image)
                if plate_crop is None:
                    st.warning(
                        "No likely plate-shaped region was found. Try a clearer, "
                        "closer image with the plate visible."
                    )
                else:
                    enlarged = cv2.resize(
                        plate_crop,
                        None,
                        fx=3,
                        fy=3,
                        interpolation=cv2.INTER_CUBIC,
                    )
                    _, thresholded_plate = cv2.threshold(
                        enlarged,
                        0,
                        255,
                        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
                    )
                    plate_text = pytesseract.image_to_string(
                        thresholded_plate,
                        config=(
                            "--psm 7 "
                            "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                        ),
                    )
                    detected_text = re.sub(r"[^A-Z0-9]", "", plate_text.upper())
                    image_col, crop_col = st.columns(2)
                    image_col.image(
                        cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB),
                        caption="Likely number-plate region",
                        use_container_width=True,
                    )
                    crop_col.image(
                        thresholded_plate,
                        caption="Plate crop for OCR",
                        channels="GRAY",
                        use_container_width=True,
                    )
                    if detected_text:
                        st.success(f"Detected characters: {detected_text}")
                    else:
                        st.info(
                            "A likely plate region was found, but no characters "
                            "could be read."
                        )
        except ValueError as error:
            st.error(str(error))
        except pytesseract.TesseractNotFoundError:
            st.error(
                "Tesseract OCR was not found. Install the Tesseract OCR engine "
                "and add its executable to PATH."
            )
        except pytesseract.TesseractError as error:
            st.error(f"Tesseract could not read this plate: {error}")

with ats_tab:
    st.subheader("Compare a resume with a job description")
    st.caption(
        "The percentage is a text-similarity estimate, not an official ATS score "
        "or a hiring decision."
    )
    resume_file = st.file_uploader(
        "Resume (PDF, TXT, PNG, JPG, or JPEG)",
        type=["pdf", "txt", "png", "jpg", "jpeg"],
        key="resume_file",
    )
    job_file = st.file_uploader(
        "Job description (PDF or TXT)",
        type=["pdf", "txt"],
        key="job_description_file",
    )
    if st.button("Compare resume", key="compare_resume"):
        if resume_file is None or job_file is None:
            st.warning("Upload both a resume and a job description to continue.")
        else:
            try:
                with st.spinner("Extracting text and comparing keywords..."):
                    resume_text = extract_uploaded_text(resume_file, is_resume=True)
                    job_text = extract_uploaded_text(job_file, is_resume=False)
                    if not resume_text or not job_text:
                        st.warning(
                            "Could not extract text from one or both files. "
                            "Check that the files contain readable text."
                        )
                    else:
                        score, missing_terms = calculate_ats_match(
                            resume_text, job_text
                        )
                        st.metric("Resume / job text similarity", f"{score}%")
                        if missing_terms:
                            st.write("Job-description keywords not found in the resume:")
                            st.write(", ".join(missing_terms[:50]))
                        else:
                            st.success("All detected job-description terms are present.")
                        with st.expander("View extracted text"):
                            resume_col, job_col = st.columns(2)
                            resume_col.text_area(
                                "Resume text", resume_text, height=240
                            )
                            job_col.text_area(
                                "Job description text", job_text, height=240
                            )
            except pytesseract.TesseractNotFoundError:
                st.error(
                    "Tesseract OCR was not found. Install the Tesseract OCR engine "
                    "and add its executable to PATH."
                )
            except pytesseract.TesseractError as error:
                st.error(f"Tesseract could not extract the document text: {error}")
            except (fitz.FileDataError, fitz.EmptyFileError) as error:
                st.error(f"Could not read the uploaded PDF: {error}")
            except UnidentifiedImageError:
                st.error("The uploaded image file could not be opened.")
            except ValueError as error:
                st.error(str(error))
            except OSError as error:
                st.error(f"Could not read the uploaded file: {error}")
