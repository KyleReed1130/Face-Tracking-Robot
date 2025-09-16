import cv2
import numpy as np
import os
import face_recognition
import pickle
import serial  
import time

# Directories and files
bush_dir = r'C:\Projects\Josh Finder 4000\train_dir\George_W_Bush'
not_bush_dir = r'C:\Projects\Josh Finder 4000\train_dir\Not_George_W_Bush'
encoding_file = r'C:\Projects\Josh Finder 4000\encodings\encodings.pkl'

# Serial port for Arduino
arduino = serial.Serial('COM3', 9600)  # Adjust COM port as needed

# readdata() was utilized for debugging

#def readdata(arduino):
#    for _ in range(3):  # Read 3 lines
#        if arduino.in_waiting > 0:  # Check if there's data available in the buffer
#            line = arduino.readline().decode('utf-8').strip()  # Read one line and decode it
#            print(f"Received: {line}")
#      qq  time.sleep(0.1)  # Slight delay to avoid overwhelming the serial buffer


# loading / creation of encodings.pkl

def load_face_encodings_from_directory(directory):
    face_encodings = []
    face_names = []
    
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(directory, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            
            if encodings:
                face_encodings.append(encodings[0])
                face_names.append(filename.split('.')[0])  
    
    return face_encodings, face_names

if os.path.exists(encoding_file):
    with open(encoding_file, 'rb') as f:
        known_face_encodings, known_face_names = pickle.load(f)
    print(f"Loaded {len(known_face_encodings)} known faces from file.")
else:
    bush_face_encodings, bush_face_names = load_face_encodings_from_directory(bush_dir)
    not_bush_face_encodings, not_bush_face_names = load_face_encodings_from_directory(not_bush_dir)
    known_face_encodings = bush_face_encodings + not_bush_face_encodings
    known_face_names = bush_face_names + not_bush_face_names
    os.makedirs(os.path.dirname(encoding_file), exist_ok=True)
    with open(encoding_file, 'wb') as f:
        pickle.dump((known_face_encodings, known_face_names), f)
    print(f"Loaded {len(known_face_encodings)} known faces.")

# cv2 is used for the laptop webcam

video_capture = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.8  
font_thickness = 2  

scale_factor = 0.5  

while True:
    # Reads frame from viideo
    ret, frame = video_capture.read()

    if not ret:
        break

    small_frame = cv2.resize(frame, (0, 0), fx=scale_factor, fy=scale_factor)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
    # face_recognition.face_encodings() function converts each detected face in a frame into an encoding
    # face_recognition.face_locations() is self explanitory
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    # frame center refers to the rectangle created around a detected face
    frame_center_x = frame.shape[1] // 2
    direction = "Center"  
    faceBool = False
    bushBool = False
    loc_value = 0

    # Recognition part of the code

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        # Checks for "Known" faces, code knows George W Bush's name and 
        # compares any identified faces to a known one and associates it with a name
        # before displaying on video.

        if face_distances[best_match_index] < 0.6: # Make sure target is close enough
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            if "George_W_Bush" in name:
                name = "Bush Detected"
                bushBool = True
            else:
                name = "Probably Not George W. Bush"
                bushBool = False

            top = int(top / scale_factor)
            right = int(right / scale_factor)
            bottom = int(bottom / scale_factor)
            left = int(left / scale_factor)

            face_center_x = (left + right) // 2

            # The following displays wether the detected face is on 
            # the center of the screen or the robot needs to turn left or right
            # Orignally designed to be controlled from here but was reworked
            # to just pass the position on to Arduino, so Arduino controlls all movement
            # Mainly usefull for just output on video and debugging

            if face_center_x < frame_center_x - 50:
                direction = "Turn Left"
                #print('face_center_x')
                #print(face_center_x)
                #loc_value = frame_center_x
            elif face_center_x > frame_center_x + 50:
                direction = "Turn Right"
                #print('face_center_x')
                #loc_value = frame_center_x
                #print(face_center_x)
                
            else:
                direction = "Center"
                #print('face_center_x')
                #loc_value = frame_center_x
                #print(loc_value)
                #print(face_center_x)

            faceBool = True

            (text_width, text_height), baseline = cv2.getTextSize(name, font, font_scale, font_thickness)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - text_height - 10), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), font, font_scale, (255, 255, 255), font_thickness)

    # Text
    cv2.putText(frame, direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    # Where data is sent to arduino
    if faceBool: # if face is present
        arduino_data = f"{int(faceBool)},{int(bushBool)},{face_center_x}\n" # send relevant data
        arduino.write(arduino_data.encode())  
        print(arduino_data.strip())
        time.sleep(1) # This is to keep pace with robot speed
    else: # if no face is present
        arduino_data = "0,0,0\n" # send default
        arduino.write(arduino_data.encode())
        print(arduino_data.strip())
        time.sleep(1) # This is to keep pace with robot speed

    # The video
    cv2.imshow("Video", frame)

    # Press 'q' to kill 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()