"""
モーターを動かしながら、物体認識付きカメラを動かし、
notebookを見つけたら止まるプログラム
物体認識にtime.sleepを入れて低負荷にした
→　成功
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
    if order == "go":
        wiringpi.digitalWrite(motor1_pin, 1)
        wiringpi.digitalWrite(motor2_pin, 0)

    elif order == "back":
        wiringpi.digitalWrite(motor1_pin, 0)
        wiringpi.digitalWrite(motor2_pin, 1)

    while True:
        if does_exist:
            wiringpi.digitalWrite(motor1_pin, 1)
            wiringpi.digitalWrite(motor2_pin, 1)


def camera():
    global does_exist
    for frame in my_camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        # machine learning
        # resize to VGG16 size(224, 224)
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
    motor1_pin = 23
    motor2_pin = 24

    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(motor1_pin, 1)
    wiringpi.pinMode(motor2_pin, 1)

    does_exist = False
    stop_item = "notebook"
    video_frame_step = 5

    th1 = threading.Thread(target=motor, name="motor", args=())
    th2 = threading.Thread(target=camera, name="camera", args=())

    th1.start()
    th2.start()