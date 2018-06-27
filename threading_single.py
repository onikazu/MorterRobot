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

print("[INFO] loading model...")
model = MobileNet(weights='imagenet')

# 対象物があるかどうかを示すフラグ
not_exist = True
graph = tf.get_default_graph()

class CameraThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = 'CameraThread'

    def run(self):
        global not_exist
        global camera
        global rawCapture
        global graph

        with graph.as_default():
        # allow the camera to warmup
            time.sleep(0.1)

            # capture frames from camera
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                # grab the raw NumPy array representing the image, then initialize the timestamp
                # and occupied/unoccupied text
                image = frame.array
                # machine learning
                # resize to mobile size(224, 224)
                img = Image.fromarray(np.uint8(image))
                img = img.resize((224, 224))
                x = img
                pred_data = np.expand_dims(x, axis=0)
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
                # 止まるように
                if result[1] == stop_item:
                        not_exist = False
                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)

                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break


class MorterThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = 'MorterThread'

    def run(self):
        global not_exist

        # 動くか判定する
        def keep_move(boolean):
            while boolean:
                time.sleep(1)
            print("ブレーキ！")
            wiringpi.digitalWrite( motor1_pin, 1 )
            wiringpi.digitalWrite( motor2_pin, 1 )

        if order == "go":
            wiringpi.digitalWrite( motor1_pin, 1 )
            wiringpi.digitalWrite( motor2_pin, 0 )
            keep_move(not_exist)

        elif order == "back":
            wiringpi.digitalWrite( motor1_pin, 0 )
            wiringpi.digitalWrite( motor2_pin, 1 )
            keep_move(not_exist)


param = sys.argv

# 第1引数
# gostraight : まっすぐ前進
# goleft : 左折
# goright : 右折
# back : まっすぐ後進
# backleft : 左へ後進
# backright : 右へ後進
# break : ブレーキ
order = param[1]

# GPIO端子の設定
motor1_pin = 23
motor2_pin = 24

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode( motor1_pin, 1 )
wiringpi.pinMode( motor2_pin, 1 )

# カメラの初期化(必ず関数の外側で！！！)
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))

# ラップトップがあるかどうかのフラグ
not_exist = True
stop_item = 'notebook'

thread1 = CameraThread()
thread2 = MorterThread()

thread1.start()
thread2.start()

thread1.join()
thread2.join()
