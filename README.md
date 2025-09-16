# Face-Tracking-Robot

> Tracked robot using OpenCV and face_recognition to detect George W. Bush. Direction (left/right/center) is sent over serial to an Arduino that steers a tracked chassis for real‑time tracking.

https://github.com/KyleReed1130/Face-Tracking-Robot

## Overview
- **Vision (Python):** Webcam frames → detect/identify target face → compute direction (Left/Right/Center).
- **Control (Arduino):** Receive serial data and drive dual-motor tracks to keep the face centered.

## Repo Contents
- `combinedv5.py` — Computer vision + serial TX (edit COM port).
- `chassis_bushfind.ino` — Chassis controller for a tracked robot.
- `requirements.txt` — Python dependencies.
- `.gitattributes` — Enables Git LFS for video and binary assets.
- `.gitignore` — Ignores build, venv, IDE, and binary clutter.
- `LICENSE` — MIT.

## Quickstart
```bash
# Clone & prepare
git clone https://github.com/KyleReed1130/Face-Tracking-Robot.git
cd Face-Tracking-Robot

# (Optional) Git LFS for video + encodings
git lfs install
git lfs track "*.mp4" "*.mov" "*.avi" "*.mkv" "*.pkl"
git add .gitattributes

# Python env
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt

# Plug in Arduino and set the correct serial port in combinedv5.py (default 9600 baud)
# Then run:
python combinedv5.py
```

## Arduino
Open `chassis_bushfind.ino` in the Arduino IDE, select your board/port, and upload.
The code reads serial messages and drives left/right/center accordingly.

## Training Data
`combinedv5.py` expects Bush and non-Bush images arranged in separate folders and will build `encodings.pkl` on first run.

## Demo Video
Add `20241210_092719.mp4` (or your own) to the repo. Because it’s large, commit it with **Git LFS**:
```bash
git lfs install
git add path/to/20241210_092719.mp4
git commit -m "Add demo video"
git push
```

## Credits
Built for ECEN4632 project work and extended into a full robot demo by Kyle Reed.
