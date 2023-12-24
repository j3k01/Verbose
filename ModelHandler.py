# import numpy as np
# from tensorflow.keras.models import load_model
# import cv2
#
# class ModelHandler:
#     def __init__(self, model_path, actions):
#         self.model = load_model(model_path)
#         self.actions = actions
#         self.sequence = []
#         self.sentence = []
#         self.predictions = []
#         self.threshold = 0.5
#
#     def extract_keypoints(self, results):
#         pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
#         # = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
#         lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
#         rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
#         return np.concatenate([pose, lh, rh]) #tu face byl jeszcze
#
#     def get_landmarks(self, results):
#         keypoints = self.extract_keypoints(results)
#         return keypoints
#
#     def prob_viz(self,res, actions, input_frame, colors):
#         output_frame = input_frame.copy()
#         res_array = np.array([res])
#         colors = [(245,117,16), (117,245,16), (16,117,245)]
#
#         for num, prob in enumerate(res_array):
#             x1, y1 = 0, int(60 + num * 40)
#             x2, y2 = int(prob * 100), int(90 + num * 40)
#
#             color_values = tuple(int(value) for value in colors[num])
#
#             cv2.rectangle(output_frame, (x1, y1), (x2, y2), color_values, -1)
#             cv2.putText(output_frame, actions[num], (x1, y1 + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
#                         cv2.LINE_AA)
#
#         return output_frame
#
#     def predict_sequence(self, sequence):
#         res = self.model.predict(np.expand_dims(sequence, axis=0))[0]
#         #print(self.actions[np.argmax(res)])
#         self.predictions.append(np.argmax(res))
#
#         if np.unique(self.predictions[-10:])[0] == np.argmax(res):
#             if res[np.argmax(res)] > self.threshold:
#                 if len(self.sentence) > 0:
#                     if self.actions[np.argmax(res)] != self.sentence[-1]:
#                         self.sentence.append(self.actions[np.argmax(res)])
#                 else:
#                     self.sentence.append(self.actions[np.argmax(res)])
#
#         if len(self.sentence) > 5:
#             self.sentence = self.sentence[-5:]
#
#         return res
#
#     def visualize_predictions(self, image, colors):
#         image = self.prob_viz(self.predictions[-1], self.actions, image, colors)  # Corrected line
#         cv2.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
#         cv2.putText(image, ' '.join(self.sentence), (3, 30),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
#         return image
#
import numpy as np
from tensorflow.keras.models import load_model

class ModelHandler:
    def __init__(self, model_path, actions):
        self.model = load_model(model_path)
        self.actions = actions
        self.sequence = []
        self.sentence = []
        self.predictions = []
        self.threshold = 0.5

    def extract_keypoints(self, results):
        pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
        lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
        rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
        return np.concatenate([pose, lh, rh])

    def get_landmarks(self, results):
        keypoints = self.extract_keypoints(results)
        return keypoints

    def prob_viz(self, res, input_frame):
        output_frame = input_frame.copy()
        for num, prob in enumerate(res):
            cv.rectangle(output_frame, (0, 60 + num * 40), (int(prob * 100), 90 + num * 40), (245, 117, 16), -1)
            cv.putText(output_frame, self.actions[num], (0, 85 + num * 40), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                       cv.LINE_AA)
        return output_frame

    def predict_sequence(self, sequence):
        res = self.model.predict(np.expand_dims(sequence, axis=0))[0]
        self.predictions.append(np.argmax(res))

        if np.unique(self.predictions[-10:])[0] == np.argmax(res):
            if res[np.argmax(res)] > self.threshold:
                if len(self.sentence) > 0:
                    if self.actions[np.argmax(res)] != self.sentence[-1]:
                        self.sentence.append(self.actions[np.argmax(res)])
                else:
                    self.sentence.append(self.actions[np.argmax(res)])

        if len(self.sentence) > 5:
            self.sentence = self.sentence[-5:]

        return res
