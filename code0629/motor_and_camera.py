"""
カメラを動かしながら、１０秒間だけモーターを動かすプログラム
"""

# for camera library
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
        time.sleep(10)
        wiringpi.digitalWrite(motor1_pin, 1)
        wiringpi.digitalWrite(motor2_pin, 1)

    elif order == "back":
        wiringpi.digitalWrite(motor1_pin, 0)
        wiringpi.digitalWrite(motor2_pin, 1)
        time.sleep(10)
        wiringpi.digitalWrite(motor1_pin, 1)
        wiringpi.digitalWrite(motor2_pin, 1)


def camera():
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q"):
            break


if __name__ == "__main__":
    param = sys.argv
    order = param[1]

    # camera setting
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(320, 240))
    time.sleep(0.1)

    # motor setting
    motor1_pin = 23
    motor2_pin = 24

    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(motor1_pin, 1)
    wiringpi.pinMode(motor2_pin, 1)

    th1 = threading.Thread(target=motor, name="motor", args=())
    th2 = threading.Thread(target=camera, name="loop_print", args=())

    th1.start()
    th2.start()