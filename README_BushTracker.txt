George Bush Tracking Robot - README.txt
==========================================

Repository one‑liner (≤350 chars):
Tracked robot that uses Python (OpenCV + face_recognition) to detect George W. Bush and send left/right/center commands over serial to an Arduino, which drives a dual‑motor tracked chassis for real‑time visual tracking. Encodings trained on Bush vs. non‑Bush images.

Overview
--------
This project detects George W. Bush in a live webcam stream and steers a tracked robot to keep the face centered. 
Python (OpenCV + face_recognition) performs detection and sends direction over serial. Arduino code drives the motors.

Included Code
-------------
- combinedv5.py  → Python vision + serial transmitter
- chassis_bushfind.ino → Arduino chassis driver (dual‑motor tracked robot)

Features
--------
- Real‑time face detection and identification (Bush vs. non‑Bush).
- Direction decision: Turn Left / Turn Right / Center.
- Serial link (USB) to Arduino for motor drive control.
- Simple proportional steering for smooth tracking.

Setup — Python
-------------
1) Python 3.9–3.11 recommended.
2) Install build tools required by dlib/face_recognition:
   - Windows: Visual Studio Build Tools + CMake
   - macOS: Xcode command line tools + CMake, `brew install cmake`
   - Linux: `sudo apt install build-essential cmake`
3) Create venv and install deps:
   python -m venv .venv
   .venv\Scripts\activate      (Windows)
   source .venv/bin/activate     (macOS/Linux)
   pip install opencv-python face_recognition numpy pyserial

Setup — Arduino
---------------
1) Open chassis_bushfind.ino in Arduino IDE.
2) Select your board (e.g., Arduino Uno) and correct serial port.
3) Upload to the board.
4) Pin mapping (parsed from code candidates):
   - PWM_PinA: 6
   - Dir_PinA01: 4
   - Dir_PinA02: 3
   - PWM_PinB: 5
   - Dir_PinB01: 2
   - Dir_PinB02: 7
   - forward: 1
   - backward: 0
5) Steering gain Kp ≈ 1/2.

Training Encodings
------------------
- Place Bush images under a Bush class folder and non‑Bush images under a separate folder (see combinedv5.py paths).
- The script creates/loads encodings.pkl and uses it to decide Bush vs. not Bush.

Usage
-----
1) Connect Arduino via USB; note the serial port (e.g., COM3 on Windows, /dev/ttyACM0 on Linux).
2) In combinedv5.py, set the correct serial port and baud (default 9600).
3) Run Python:
   python combinedv5.py
4) The on‑screen overlay shows detection status and direction. Arduino receives direction data to drive the tracks.

Wiring (Text Diagram)
---------------------
Power:
- Use a dedicated battery pack for the motors (appropriate voltage for your driver/motors).
- Common the grounds: Motor battery GND → Motor driver GND → Arduino GND → USB GND.

Signals:
- Arduino PWM pins → Motor driver PWM/EN inputs (Left/Right channels).
- Arduino DIR pins → Motor driver IN1/IN2 (per channel).
- Motor driver outputs → Left DC motor / Right DC motor.

Example (generic TB6612FNG/L298N style):
- LEFT channel: ENA(PWM), IN1, IN2 → Left motor terminals (M1A/M1B).
- RIGHT channel: ENB(PWM), IN3, IN4 → Right motor terminals (M2A/M2B).
- Supply the driver VM (motor voltage) from battery; Vcc (logic) from Arduino 5V (check your driver specs).

Tuning Tips
-----------
- If turns are too aggressive or sluggish, adjust Kp in the .ino.
- Add a deadband around image center (±50 px) to reduce jitter (already used in combinedv5.py).
- Cap max PWM for smoother motion on lightweight chassis.

Troubleshooting
---------------
- If no movement: verify serial port matches in combinedv5.py and that Arduino is receiving (use Serial Monitor).
- If dlib/face_recognition fails to build: confirm CMake and compiler toolchain are installed.
- If motors spin backward: swap IN1/IN2 (or reverse motor leads) for that side.

Notes
-----
- combinedv5.py currently uses a Windows path layout and COM3 by default; update paths/port for your machine.
- Face threshold can be tuned (default 0.6); lower for stricter recognition.
