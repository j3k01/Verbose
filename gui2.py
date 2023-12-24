import cv2 as cv
import numpy as np
from MediapipeHandler import MediapipeHandler
from ModelHandler import ModelHandler
from pathlib import Path
from PIL import Image, ImageTk
import tkinter as Tk
from tkinter import Tk, Canvas, Button, PhotoImage
import threading



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\dell\Desktop\studia\inzynierka\gui2\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def start_opencv_processing():
    global opencv_processing
    opencv_processing = True
    process_frames()

def stop_opencv_processing():
    global opencv_processing
    opencv_processing = False

def process_frames():
    ret, frame = cap.read()

    if opencv_processing:
        image, results = MediapipeHandler.process_frame(frame)

        MediapipeHandler.draw_landmarks(image, results)

        keypoints = ModelHandler.get_landmarks(results)
        ModelHandler.sequence.append(keypoints)
        ModelHandler.sequence = ModelHandler.sequence[-30:]

        if len(ModelHandler.sequence) == 30:
            res = ModelHandler.predict_sequence(ModelHandler.sequence)
            image = ModelHandler.visualize_predictions(image, actions)

        img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(img))
        canvas.create_image(0, 0, anchor='nw', image=photo)
        canvas.photo = photo

    if cv.waitKey(10) & 0xFF == ord('q'):
        return

    window.after(10, process_frames)


actions = np.array(['hello', 'thanks', 'ok'])
MediapipeHandler = MediapipeHandler()
ModelHandler = ModelHandler('action.h5', actions)
colors = [(245, 117, 16), (117, 245, 16), (16, 117, 245)]

opencv_processing = False

cap = cv.VideoCapture(0)

window = Tk()
window.geometry("966x650")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=736,
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
    command=start_opencv_processing,
    relief="flat"
)
button_1.place(
    x=699.0,
    y=303.0,
    width=190.0,
    height=53.0
)

# # Add a button to stop OpenCV processing
# button_stop_opencv = Button(
#     text="Stop OpenCV",
#     command=stop_opencv_processing
# )
# button_stop_opencv.place(
#     x=699.0,
#     y=530.0,
#     width=190.0,
#     height=30.0
# )

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
    command=lambda: print("stop_opencv_processing"),
    relief="flat"
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
    command=lambda: print("button_4 clicked"),
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
