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
