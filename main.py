import mediapipe as mp
import cv2
import serial
import time

# Initialize Mediapipe and Serial connection to Arduino
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
cap = cv2.VideoCapture(0)

# Replace 'COM3' with your Arduino port
arduino = serial.Serial('COM3', 9600)
time.sleep(2)  # Wait for the serial connection to initialize

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to RGB for Mediapipe processing
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        # Check if landmarks are detected
        if results.pose_landmarks:
            # Extract relevant landmarks
            left_wrist_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y
            right_wrist_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y
            left_shoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y
            right_shoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y

            # Condition: Turn on the light when both wrists are above shoulders
            if left_wrist_y < left_shoulder_y and right_wrist_y < right_shoulder_y:
                arduino.write(b'1')  # Send '1' to Arduino to turn on the light
            else:
                arduino.write(b'0')  # Send '0' to Arduino to turn off the light

        # Display the frame
        cv2.imshow('Pose Detection', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()
