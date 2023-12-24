import os
import cv2 as cv
import numpy as np
import mediapipe as mp
from MediapipeHandler import MediapipeHandler

class DataHandler:
    def __init__(self, data_path, actions, no_sequences=30, sequence_length=30):
        self.data_path = data_path
        self.actions = actions
        self.no_sequences = no_sequences
        self.sequence_length = sequence_length
        self.mediapipe_handler = MediapipeHandler()

    def collect_data(self, cap, model_handler):
        for action in self.actions:
            for sequence in range(self.no_sequences):
                try:
                    os.makedirs(os.path.join(self.data_path, action, str(sequence)))
                except:
                    pass

                self.collect_sequence_data(cap, model_handler, action, sequence)

        cap.release()
        cv.destroyAllWindows()

    def collect_sequence_data(self, cap, model_handler, action, sequence):
        with mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as model:
            for frame_num in range(self.sequence_length):
                ret, frame = cap.read()

                image, results = self.mediapipe_handler.process_frame(frame)
                self.mediapipe_handler.draw_landmarks(image, results)

                if frame_num == 0:
                    cv.putText(image, 'STARTING COLLECTION', (120, 200),
                               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv.LINE_AA)
                    cv.putText(image, 'Collecting frames for {} Video Number {}'.format(action, sequence),
                               (15, 12), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)
                    cv.imshow('Camera mediapipe', image)
                    cv.waitKey(2000)
                else:
                    cv.putText(image, 'Collecting frames for {} Video Number {}'.format(action, sequence),
                               (15, 12), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)
                    cv.imshow('Camera mediapipe', image)

                keypoints = model_handler.get_landmarks(results)
                npy_path = os.path.join(self.data_path, action, str(sequence), str(frame_num))
                np.save(npy_path, keypoints)

                mirrored_frame = cv.flip(image, 1)
                cv.imshow('Camera mediapipe', mirrored_frame)

                if cv.waitKey(10) & 0xFF == ord('q'):
                    break
