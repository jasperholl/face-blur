
# Face Blur Tool

This tool automatically detects and blurs faces in images using a YOLOv8 face detection model.

## Features

- Select a folder with images (JPG, JPEG, PNG).
- Automatically detects faces and blurs them.
- Saves blurred images in a new subfolder called `output_blurred`.

## How to use

1. Download the YOLOv8 face detection model file `yolov8n-face.pt` and place it in the same folder as the script or executable.

   **Download YOLOv8 face model:**
   https://github.com/ternaus/Ultra-Light-Fast-Generic-Face-Detector-1MB/releases/download/v0.0.0/yolov8n-face.pt

2. Run the `blur_faces_gui.py` script using:

```bash
python blur_faces_gui.py
```

Or if you have an executable, simply double-click it.

3. Select your input folder with images. The output will be saved in `output_blurred` inside your selected folder.

## Requirements

Install required Python libraries:

```bash
pip install ultralytics opencv-python pillow tkinter torch torchvision torchaudio --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org
```

## License

This project is provided as-is. Check Ultralytics' license terms if you use their YOLOv8 models commercially. By default, internal (non-commercial or testing) use is permitted, but for commercial applications you may need a paid license from Ultralytics.

---

**Author:** Jasper Holl  
**Company:** Sweco NL
