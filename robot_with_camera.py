# カメラ動作のためのライブラリ
from picamera.array import PiRGBArray
from picamera import PiCamera
from keras.applications.mobilenet import MobileNet, preprocess_input, decode_predictions
from keras.preprocessing import image
from PIL import Image
import RPi.GPIO as GPIO
import numpy as np
import os
import cv2

# 並列処理
import threading

# GPIOを制御するライブラリ
import wiringpi
# タイマーのライブラリ
import time
# 引数取得
import sys

# 動くか判定する
def keep_move(boolean):
    while boolean:
        print('There are no laptops. keep moving!')
    print("ブレーキ！")
    wiringpi.digitalWrite( right_forward_pin, 1 )
    wiringpi.digitalWrite( left_forward_pin, 1 )
    wiringpi.digitalWrite( right_back_pin, 1 )
    wiringpi.digitalWrite( left_back_pin, 1 )


# モーターの動作に関する関数
def morter(exists_laptop):
    if order == "goright":
        wiringpi.digitalWrite( right_forward_pin, 1 )
        wiringpi.digitalWrite( right_back_pin, 0 )
        keep_move(exists_laptop)
    elif order == "backright":
        wiringpi.digitalWrite( right_forward_pin, 0 )
        wiringpi.digitalWrite( right_back_pin, 1 )
        keep_move(exists_laptop)
    elif order == "goleft":
        wiringpi.digitalWrite( left_forward_pin, 1 )
        wiringpi.digitalWrite( left_back_pin, 0 )
        keep_move(exists_laptop)
    elif order == "backleft":
        wiringpi.digitalWrite( left_forward_pin, 0 )
        wiringpi.digitalWrite( left_back_pin, 1 )
        keep_move(exists_laptop)
    elif order == "gostraight":
        wiringpi.digitalWrite( left_forward_pin, 1 )
        wiringpi.digitalWrite( left_back_pin, 0 )
        wiringpi.digitalWrite( right_forward_pin, 1 )
        wiringpi.digitalWrite( right_back_pin, 0 )
        keep_move(exists_laptop)
    elif order == "back":
        wiringpi.digitalWrite( left_forward_pin, 0 )
        wiringpi.digitalWrite( left_back_pin, 1 )
        wiringpi.digitalWrite( right_forward_pin, 0 )
        wiringpi.digitalWrite( right_back_pin, 1 )
        keep_move(exists_laptop)

# カメラの動作に関する関数
def camera():
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



if __name__ == "__main__":
    # 引数
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
    right_forward_pin = 4
    right_back_pin = 17
    left_back_pin = 11
    left_forward_pin = 9

    # GPIO出力モードを1に設定する(onにするということ)
    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode( right_forward_pin, 1 )
    wiringpi.pinMode( right_back_pin, 1 )
    wiringpi.pinMode( left_back_pin, 1 )
    wiringpi.pinMode( left_forward_pin, 1 )

    # ラップトップがあるかどうかのフラグ
    not_exist = True
    stop_item = 'notebook'

    print("[INFO] loading model...")
    model = MobileNet(weights='imagenet')

    thread_1 = threading.Thread(target=morter)
    thread_2 = threading.Thread(target=camera, args=(not_exist,))

    thread_1.start()
    thread_2.start()
