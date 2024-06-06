import cv2
import face_recognition
import threading
import queue
import serial
import pyttsx3
engine = pyttsx3.init()

arduino_port = 'COM4'  # Adjust to your virtual serial port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

known_image = face_recognition.load_image_file("ayoub.jpg")
known_face_encoding = face_recognition.face_encodings(known_image)[0]

frame_queue = queue.Queue(maxsize=10)

ip_camera_url = "http://192.168.43.55:8080/video"


def capture_frames():
    cap = cv2.VideoCapture(ip_camera_url)
    if not cap.isOpened():
        print("Error: Unable to open video stream")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if not frame_queue.full():
            frame_queue.put(frame)

    cap.release()


capture_thread = threading.Thread(target=capture_frames, daemon=True)
capture_thread.start()
def announce_recognition(message):
    # pyttsx3.speak(message)
    engine.say(message)
    engine.runAndWait()
    if engine._inLoop:
        engine.endLoop()

recognized = False
first_time = True
# Main processing loop
# while not recognized:
while True:
    if not frame_queue.empty():
        frame = frame_queue.get()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                [known_face_encoding], face_encoding)
            name = "Unknown"

            if True in matches:
                name = "Known Person"
                print("Person recognized, opening door")
                if first_time or not recognized:
                    ser.write(b'o')
                    announce_thread = threading.Thread(target=announce_recognition,args=("Welcome..sir..Door is openning for 5 seconds",))
                    announce_thread.start()
                    first_time = False
                recognized = True
                break
            else:
                if first_time or recognized:
                    ser.write(b'c')
                    announce_thread = threading.Thread(target=announce_recognition, args=("Unknown person detected",))
                    announce_thread.start()
                    first_time = False
                recognized = False
                break

        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)

        display_frame = cv2.resize(frame, (600, 400))

        cv2.imshow('Video', display_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
ser.close()