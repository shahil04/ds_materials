import cv2
import os
import torch
import pytesseract
import pandas as pd
import yolov5
import re
from scipy.spatial.distance import euclidean
import easyocr

# ==== Paths ====
video_path = r"1482016-hd_1920_1080_25fps.mp4"
model_path = r"best.pt"
output_folder = 'detected_plates'
os.makedirs(output_folder, exist_ok=True)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

print("🔄 Loading YOLOv5 model...")
model = yolov5.load(model_path)
print("✅ YOLOv5 model loaded.")

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"❌ Error opening video: {video_path}")
    exit()

print("▶️ Starting license plate detection and tracking...")

def clean_plate_text(text):
    text = text.upper()
    return re.sub(r'[^A-Z0-9]', '', text)

def get_centroid(box):
    x1, y1, x2, y2 = box
    return ((x1 + x2)//2, (y1 + y2)//2)

max_distance = 50  # pixels

car_tracks = {}
car_plates = {}
car_images = {}
next_car_id = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = model(frame).xyxy[0]
    current_centroids = []

    for *box, conf, cls in detections:
        x1, y1, x2, y2 = map(int, box)
        centroid = get_centroid(box)
        current_centroids.append((x1, y1, x2, y2, centroid))

    matched_cars = set()
    for x1, y1, x2, y2, centroid in current_centroids:
        matched_id = None
        min_dist = float('inf')

        for car_id, last_centroid in car_tracks.items():
            dist = euclidean(centroid, last_centroid)
            if dist < max_distance and dist < min_dist:
                min_dist = dist
                matched_id = car_id

        if matched_id is None:
            next_car_id += 1
            matched_id = next_car_id

        car_tracks[matched_id] = centroid
        matched_cars.add(matched_id)

        plate_img = frame[y1:y2, x1:x2]
        if plate_img.size == 0:
            continue

        gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        text = pytesseract.image_to_string(thresh, config='--psm 7')
        plate_text = clean_plate_text(text)

        if len(plate_text) < 5:
            plate_text = None

        if plate_text:
            prev_text = car_plates.get(matched_id, "")
            if len(plate_text) > len(prev_text):
                car_plates[matched_id] = plate_text

                if matched_id not in car_images:
                    filename = f"{plate_text}_{matched_id}.jpg"
                    filepath = os.path.join(output_folder, filename)
                    cv2.imwrite(filepath, plate_img)
                    car_images[matched_id] = filename
                    print(f"✅ Saved plate {plate_text} for car {matched_id}")

    missing_cars = set(car_tracks.keys()) - matched_cars
    for car_id in missing_cars:
        del car_tracks[car_id]

    cv2.imshow("Plate Detection & Tracking", frame)
    if cv2.waitKey(1) == 27:
        print("Exiting early.")
        break

cap.release()
cv2.destroyAllWindows()

# ===== Post-process saved images with EasyOCR and save final CSV =====

print("\n🔎 Post-processing saved plate images with EasyOCR...")

reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if available

final_results = []

for car_id, img_file in car_images.items():
    img_path = os.path.join(output_folder, img_file)
    if not os.path.isfile(img_path):
        print(f"⚠️ Image not found: {img_path}")
        continue

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"⚠️ Could not read image: {img_path}")
        continue

    _, img_thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    ocr_results = reader.readtext(img_thresh)

    ocr_text = ''.join([res[1] for res in ocr_results]).upper()
    ocr_text_clean = re.sub(r'[^A-Z0-9]', '', ocr_text)

    if len(ocr_text_clean) < 5:
        ocr_text_clean = car_plates.get(car_id, "UNKNOWN")

    final_results.append({
        'CarID': car_id,
        'LicensePlate': ocr_text_clean,
        'Image': img_file
    })

    print(f"Car {car_id}: Final OCR text = {ocr_text_clean}")

df_final = pd.DataFrame(final_results)
df_final.to_csv('license_plates_final.csv', index=False)
print("✅ Saved final license plates to license_plates_final.csv")
print(f"\n🎉 Done! Unique cars detected: {len(car_plates)}")
