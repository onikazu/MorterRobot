"""
モーターを２つ回し、notebookを見つけたら止まるプログラム
"""

import wiringpi
from picamera.array import PiRGBArray
from picamera import PiCamera
from keras.applications.mobilenet import MobileNet, preprocess_input, decode_predictions
from keras.preprocessing import image
from PIL import Image
import numpy as np
import cv2
import tensorflow as tf

import threading, time, datetime
import sys
import os

from picamera.array import PiRGBArray
from picamera import PiCamera
from keras.preprocessing import image
from PIL import Image
import numpy as np
import cv2

# for motor library
import wiringpi

import threading, time, datetime
import sys
import os


def motor():
    if order == "goright":
        wiringpi.digitalWrite(right_forward_pin, 1)
        wiringpi.digitalWrite(right_back_pin, 0)
    elif order == "backright":
        wiringpi.digitalWrite(right_forward_pin, 0)
        wiringpi.digitalWrite(right_back_pin, 1)
    elif order == "goleft":
        wiringpi.digitalWrite(left_forward_pin, 1)
        wiringpi.digitalWrite(left_back_pin, 0)
    elif order == "backleft":
        wiringpi.digitalWrite(left_forward_pin, 0)
        wiringpi.digitalWrite(left_back_pin, 1)
    elif order == "gostraight":
        wiringpi.digitalWrite(left_forward_pin, 1)
        wiringpi.digitalWrite(left_back_pin, 0)
        wiringpi.digitalWrite(right_forward_pin, 1)
        wiringpi.digitalWrite(right_back_pin, 0)
    elif order == "back":
        wiringpi.digitalWrite(left_forward_pin, 0)
        wiringpi.digitalWrite(left_back_pin, 1)
        wiringpi.digitalWrite(right_forward_pin, 0)
        wiringpi.digitalWrite(right_back_pin, 1)
    while True:
        if does_exist:
            wiringpi.digitalWrite(right_forward_pin, 1)
            wiringpi.digitalWrite(left_forward_pin, 1)
            wiringpi.digitalWrite(right_back_pin, 1)
            wiringpi.digitalWrite(left_back_pin, 1)


def camera():
    global does_exist
    for frame in my_camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        # machine learning
        # resize to mobile net size(224, 224)
        img = Image.fromarray(np.uint8(image))
        img = img.resize((224, 224))
        x = img
        pred_data = np.expand_dims(x, axis=0)
        with graph.as_default():
            preds = model.predict(preprocess_input(pred_data))
            results = decode_predictions(preds, top=1)[0]
            for result in results:
                # print(result)
                label = result[1]
                accu = str(result[2])
            # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # show the frame
            new_label = label + accu
            image = cv2.putText(image, new_label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF

        if label == stop_item:
            does_exist = True

        rawCapture.truncate(0)
        time.sleep(video_frame_step)
        if key == ord("q"):
            break


if __name__ == "__main__":
    print("[INFO] loading model...")
    model = MobileNet(weights='imagenet')
    print("[INFO] loading is done")
    graph = tf.get_default_graph()

    param = sys.argv
    order = param[1]

    # camera setting
    my_camera = PiCamera()
    my_camera.resolution = (320, 240)
    my_camera.framerate = 32
    rawCapture = PiRGBArray(my_camera, size=(320, 240))
    time.sleep(0.1)

    # motor setting
    right_forward_pin = 4
    right_back_pin = 17
    left_back_pin = 11
    left_forward_pin = 9

    # GPIO出力モードを1に設定する(onにするということ)
    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(right_forward_pin, 1)
    wiringpi.pinMode(right_back_pin, 1)
    wiringpi.pinMode(left_back_pin, 1)
    wiringpi.pinMode(left_forward_pin, 1)

    does_exist = False
    stop_item = "notebook"
    video_frame_step = 5

    th1 = threading.Thread(target=motor, name="motor", args=())
    th2 = threading.Thread(target=camera, name="camera", args=())

    th1.start()
    th2.start()
