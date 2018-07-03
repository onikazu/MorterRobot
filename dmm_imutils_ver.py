from keras.preprocessing.image import img_to_array
from keras.models import load_model
from keras.applications.mobilenet import MobileNet, preprocess_input, decode_predictions
import wiringpi
import tensorflow as tf

from imutils.video import VideoStream
from threading import Thread
import numpy as np
import imutils
import time
import cv2
import os
import sys


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
    while True:
        global does_exist
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # prepare the image to be classified by our deep learning network
        image = cv2.resize(frame, (28, 28))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        pred_data = np.expand_dims(image, axis=0)
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

        # rawCapture.truncate(0)
        if key == ord("q"):
            break


if __name__ == "__main__":
    print("[INFO] loading model...")
    model = MobileNet(weights='imagenet')
    print("[INFO] loading is done")
    print("[INFO] starting video stream...")
    graph = tf.get_default_graph()
    # vs = VideoStream(src=0).start()
    vs = VideoStream(usePiCamera=True).start()
    time.sleep(5.0)

    param = sys.argv
    order = param[1]

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

    th1 = Thread(target=motor, name="motor", args=())
    th2 = Thread(target=camera, name="camera", args=())
