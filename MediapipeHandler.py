import cv2 as cv
import mediapipe as mp
import numpy as np
import time

class MediapipeHandler:
    def __init__(self):
        self.mp_holistic = mp.solutions.holistic
        self.mp_drawing = mp.solutions.drawing_utils
        self.holistic = self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def start_tracking_for_duration(self, cap, duration=10):
        start_time = time.time()

        while cap.isOpened():
            if time.time() - start_time > duration:
                break

            ret, frame = cap.read()
            frame = cv.flip(frame, 1)

            image, results = self.process_frame(frame)
            self.draw_landmarks(image, results)

            cv.imshow('OpenCV Feed', image)

            if cv.waitKey(10) & 0xFF == ord('q'):
                break

    def process_frame(self, frame):
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.holistic.process(image)
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        return image, results


    def draw_landmarks(self, image, results):
        landmark_drawing_spec = self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1)
        connection_drawing_spec = self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1)
        landmark_drawing_spec_hand = self.mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2)
        connection_drawing_spec_hand = self.mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1)

        #self.mp_drawing.draw_landmarks(image, results.face_landmarks, self.mp_holistic.FACEMESH_TESSELATION,
         #                         landmark_drawing_spec=landmark_drawing_spec,
          #                        connection_drawing_spec=connection_drawing_spec)
        self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS,
                                  landmark_drawing_spec=landmark_drawing_spec,
                                  connection_drawing_spec=connection_drawing_spec)
        self.mp_drawing.draw_landmarks(image, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                  landmark_drawing_spec=landmark_drawing_spec_hand,
                                  connection_drawing_spec=connection_drawing_spec_hand)
        self.mp_drawing.draw_landmarks(image, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                  landmark_drawing_spec=landmark_drawing_spec_hand,
                                  connection_drawing_spec=connection_drawing_spec_hand)
