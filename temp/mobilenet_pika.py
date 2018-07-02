# source
# http://walking-succession-falls.com/raspberrypi%E3%81%AE%E3%82%AB%E3%83%A1%E3%83%A9%E3%83%A2%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%ABv2%E3%81%8B%E3%82%89%E6%B5%81%E3%82%8C%E3%82%8B%E3%82%B9%E3%83%88%E3%83%AA%E3%83%BC%E3%83%9F%E3%83%B3/

from picamera.array import PiRGBArray
from picamera import PiCamera
from keras.applications.mobilenet import MobileNet, preprocess_input, decode_predictions
from keras.preprocessing import image
from PIL import Image
import RPi.GPIO as GPIO
import numpy as np
import sys, os
import time
import cv2

COUNT = 3
PIN = 3

print("[INFO] loading model...")
model = MobileNet(weights='imagenet')

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    # machine learning
    # resize to VGG16 size(224, 224)
    img = Image.fromarray(np.uint8(image))
    img = img.resize((224, 224))
    x = img
    pred_data = np.expand_dims(x, axis=0)
    preds = model.predict(preprocess_input(pred_data))
    results = decode_predictions(preds, top=1)[0]
    for result in results:
        # print(result)
        label = result[1]
        accu  = str(result[2])
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # show the frame
    new_label = label + accu
    image = cv2.putText(image, new_label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    # ピカ処理
    if(result[1]=='notebook'):
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(PIN,GPIO.OUT)
            for _ in range(COUNT):
                GPIO.output(PIN,True)
                time.sleep(1.0)
                GPIO.output(PIN,False)
                time.sleep(1.0)
            GPIO.cleanup()
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    time.sleep(3)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
