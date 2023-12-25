import time
import keyboard
import cv2 as cv
import numpy as np
from MediapipeHandler import MediapipeHandler
from ModelHandler import ModelHandler
from DataHandler import DataHandler
from VoiceHandler import VoiceHandler
from pathlib import Path
from PIL import Image, ImageTk
import tkinter as Tk
from tkinter import Tk, Canvas, Button, PhotoImage, Label, Toplevel
import threading
import os
from sklearn.metrics import multilabel_confusion_matrix, accuracy_score
from scipy import stats
from gtts import gTTS

sign_array = np.array(['nice','meet','you','hello2','no2','yes2','thanks2','ok2','iloveyou2','have','day','help'])

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\dell\Desktop\studia\inzynierka\gui2\build\assets\frame0")
actions = sign_array
data_path = os.path.join('data')
data_handler = DataHandler(data_path, actions, no_sequences=30, sequence_length=30)
mediapipe_handler = MediapipeHandler()





def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def show_author_info():
    if not hasattr(show_author_info, 'author_info_window') or not show_author_info.author_info_window:
        show_author_info.author_info_window = Toplevel(window)
        show_author_info.author_info_window.title("Author Information")
        show_author_info.author_info_window.resizable(False, False)
        show_author_info.author_info_window.geometry("300x100")
        author_info_label = Label(show_author_info.author_info_window, text="Author: Jakub Kostka\nContact: golomp pocztowy")
        author_info_label.pack(padx=20, pady=20)

        show_author_info.author_info_window.protocol("WM_DELETE_WINDOW", close_author_info_window)

def close_author_info_window():
    show_author_info.author_info_window.destroy()
    show_author_info.author_info_window = None



def start_opencv_processing():
    global opencv_processing
    opencv_processing = True
    process_frames()

def start_collecting_data():
    global collecting_data
    collecting_data = True
    threading.Thread(target=collect_data_thread).start()


def collect_data_thread():
    global collecting_data
    with MediapipeHandler.holistic as model:
        mediapipe_handler.start_tracking_for_duration(cap)
        data_handler.collect_data(cap, ModelHandler)
    collecting_data = False


def stop_opencv_processing():
    global opencv_processing
    opencv_processing = False

def process_frames():
    ret, frame = cap.read()

    if opencv_processing:
        frame = cv.flip(frame, 1)
        image, results = MediapipeHandler.process_frame(frame)

        MediapipeHandler.draw_landmarks(image, results)

        keypoints = ModelHandler.get_landmarks(results)
        ModelHandler.sequence.append(keypoints)
        ModelHandler.sequence = ModelHandler.sequence[-30:]

        if len(ModelHandler.sequence) == 30:
            res = ModelHandler.predict_sequence(ModelHandler.sequence)

            if np.max(res) > 0.60:
                max_index = np.argmax(res)
                if max_index < len(actions):
                    language = 'en'
                    print(f"Detected sign: {actions[max_index]} with accuracy: {res[max_index]}")
                    if actions[max_index] == 'nice' and keyboard.is_pressed('ctrl'):
                        voice_handler = VoiceHandler(actions[max_index])
                        voice_handler.play_sound()
                    elif actions[max_index] == 'meet' and keyboard.is_pressed('ctrl'):
                        voice_handler = VoiceHandler(actions[max_index])
                        voice_handler.play_sound()
                    elif actions[max_index] == 'you' and keyboard.is_pressed('ctrl'):
                        voice_handler = VoiceHandler(actions[max_index])
                        voice_handler.play_sound()
                    elif actions[max_index] == 'hello2' and keyboard.is_pressed('ctrl'):
                        voice_handler = VoiceHandler(actions[max_index])
                        voice_handler.play_sound()
                    elif actions[max_index] == 'no2' and keyboard.is_pressed('ctrl'):
                        voice_handler = VoiceHandler(actions[max_index])
                        voice_handler.play_sound()
                    elif actions[max_index] == 'yes2' and keyboard.is_pressed('ctrl'):
                        voice_handler = VoiceHandler(actions[max_index])
                        voice_handler.play_sound()
                    elif actions[max_index] == 'thanks2' and keyboard.is_pressed('ctrl'):
                        voice_handler = VoiceHandler(actions[max_index])
                        voice_handler.play_sound()
                    elif actions[max_index] == 'ok2' and keyboard.is_pressed('ctrl'):
                        voice_handler = VoiceHandler(actions[max_index])
                        voice_handler.play_sound()
                    elif actions[max_index] == 'iloveyou2' and keyboard.is_pressed('ctrl'):
                        voice_handler = VoiceHandler(actions[max_index])
                        voice_handler.play_sound()
                    elif actions[max_index] == 'have' and keyboard.is_pressed('ctrl'):
                        voice_handler = VoiceHandler(actions[max_index])
                        voice_handler.play_sound()
                    elif actions[max_index] == 'day' and keyboard.is_pressed('ctrl'):
                        voice_handler = VoiceHandler(actions[max_index])
                        voice_handler.play_sound()
                    elif actions[max_index] == 'help' and keyboard.is_pressed('ctrl'):
                        voice_handler = VoiceHandler(actions[max_index])
                        voice_handler.play_sound()






        img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(img))
        canvas.create_image(0, 0, anchor='nw', image=photo)
        canvas.photo = photo

    if cv.waitKey(10) & 0xFF == ord('q'):
        return

    window.after(10, process_frames)


def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv.rectangle(output_frame, (0,60+num*40), (int(prob*100), 90+num*40), colors[num], -1)
        cv.putText(output_frame, actions[num], (0, 85+num*40), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv.LINE_AA)

    return output_frame

def process_frames2():
    model.load_weights('actionNewAll.h5')
    yhat = model.predict(sequence)
    ytrue = np.argmax(y_test, axis=1).tolist()
    yhat = np.argmax(yhat, axis=1).tolist()
    multilabel_confusion_matrix(ytrue, yhat)
    accuracy_score(ytrue, yhat)
    colors = [(245, 117, 16), (117, 245, 16), (16, 117, 245)]
    sequence = []
    sentence = []
    predictions = []
    threshold = 0.5

    cap = cv.VideoCapture(0)
    # Set mediapipe model
    with mediapipe_handler.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.7) as holistic:
        while cap.isOpened():

            ret, frame = cap.read()

            image, results = mediapipe_detection(frame, holistic)
            print(results)

            draw_styled_landmarks(image, results)

            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-30:]

            if len(sequence) == 30:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                print(actions[np.argmax(res)])
                predictions.append(np.argmax(res))

            # 3. Viz logic
            if len(predictions) >= 10 and len(np.unique(predictions[-10:])) > 0 and np.unique(predictions[-10:])[0] == np.argmax(res):
                if res[np.argmax(res)] > threshold:
                    if len(sentence) > 0:
                        if actions[np.argmax(res)] != sentence[-1]:
                            sentence.append(actions[np.argmax(res)])
                    else:
                        sentence.append(actions[np.argmax(res)])

                if len(sentence) > 5:
                    sentence = sentence[-5:]

                image = prob_viz(res, actions, image, colors)

            cv.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
            cv.putText(image, ' '.join(sentence), (3, 30),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)

            cv.imshow('OpenCV Feed', image)

            if cv.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        cv.destroyAllWindows()

actions = sign_array
MediapipeHandler = MediapipeHandler()
ModelHandler = ModelHandler('C:\\Users\\dell\\Desktop\\studia\\inzynierka\\actionAll2312.h5', actions)
colors = [(245, 117, 16), (117, 245, 16), (16, 117, 245)]



opencv_processing = False


cap = cv.VideoCapture(0)

window = Tk()
window.geometry("966x716")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=716,
    width=966,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    367.0,
    431.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=start_collecting_data,
    relief="flat"
)
button_1.place(
    x=699.0,
    y=303.0,
    width=190.0,
    height=53.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    772.0,
    113.0,
    image=image_image_2
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=start_opencv_processing,
    relief="flat"
)
button_2.place(
    x=699.0,
    y=227.0,
    width=190.0,
    height=53.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=show_author_info,
    relief="flat",
    text="Author Information",
)
button_3.place(
    x=699.0,
    y=379.0,
    width=190.0,
    height=53.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: exit(),
    relief="flat"
)
button_4.place(
    x=699.0,
    y=455.0,
    width=190.0,
    height=53.0
)
window.resizable(False, False)
window.mainloop()




