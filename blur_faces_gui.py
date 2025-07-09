import os
import sys
import cv2
import numpy as np
from tkinter import Tk, filedialog, messagebox
from ultralytics import YOLO

def resource_path(relative_path):
    """Pad-oplossing voor PyInstaller .exe builds"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

MODEL_PATH = resource_path("yolov8n-face.pt")
model = YOLO(MODEL_PATH)

def detect_faces(image):
    results = model.predict(image, conf=0.3, imgsz=1280, verbose=False)
    return results[0].boxes.xyxy.cpu().numpy() if results[0].boxes is not None else []

def merge_boxes(original, mirrored, width):
    all_boxes = original.copy()
    for x1, y1, x2, y2 in mirrored:
        mirrored_box = [width - x2, y1, width - x1, y2]
        all_boxes.append(mirrored_box)
    return np.array(all_boxes)

def is_valid_box(x1, y1, x2, y2):
    w, h = x2 - x1, y2 - y1
    ratio = w / h if h else 0
    return 30 < w < 300 and 30 < h < 300 and 0.5 <= ratio <= 2.0

def main():
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Selecteer een map met foto's")

    if not folder:
        messagebox.showinfo("Annuleren", "Geen map geselecteerd.")
        return

    output_folder = os.path.join(folder, "output_anonimiseerd")
    os.makedirs(output_folder, exist_ok=True)

    files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not files:
        messagebox.showinfo("Geen foto's", "Geen afbeeldingen gevonden in deze map.")
        return

    for filename in files:
        input_path = os.path.join(folder, filename)
        output_path = os.path.join(output_folder, filename)
        image = cv2.imread(input_path)
        height, width = image.shape[:2]

        orig = detect_faces(image)
        flipped = detect_faces(cv2.flip(image, 1))
        all_boxes = merge_boxes(orig.tolist(), flipped.tolist(), width)

        valid_boxes = [
            (int(x1), int(y1), int(x2), int(y2))
            for x1, y1, x2, y2 in all_boxes if is_valid_box(x1, y1, x2, y2)
        ]

        for x1, y1, x2, y2 in valid_boxes:
            roi = image[y1:y2, x1:x2]
            if roi.size > 0:
                image[y1:y2, x1:x2] = cv2.GaussianBlur(roi, (99, 99), 30)

        cv2.imwrite(output_path, image)
        print(f"✅ {filename} opgeslagen")

    messagebox.showinfo("Klaar", f"{len(files)} afbeelding(en) verwerkt.\nOutput: {output_folder}")

if __name__ == "__main__":
    main()
