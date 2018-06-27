# daemonにモーター処理を、メインスレッドにカメラの処理を。。。
import wiringpi
import os
import cv2
from keras.preprocessing import image
from PIL import Image
from picamera.array import PiRGBArray
from picamera import PiCamera

import threading
import time
import sys

def moter():
    if order == "goright":
        wiringpi.digitalWrite( right_forward_pin, 1 )
        wiringpi.digitalWrite( right_back_pin, 0 )
    elif order == "backright":
        wiringpi.digitalWrite( right_forward_pin, 0 )
        wiringpi.digitalWrite( right_back_pin, 1 )
    elif order == "goleft":
        wiringpi.digitalWrite( left_forward_pin, 1 )
        wiringpi.digitalWrite( left_back_pin, 0 )
    elif order == "backleft":
        wiringpi.digitalWrite( left_forward_pin, 0 )
        wiringpi.digitalWrite( left_back_pin, 1 )
    elif order == "gostraight":
        wiringpi.digitalWrite( left_forward_pin, 1 )
        wiringpi.digitalWrite( left_back_pin, 0 )
        wiringpi.digitalWrite( right_forward_pin, 1 )
        wiringpi.digitalWrite( right_back_pin, 0 )
    elif order == "back":
        wiringpi.digitalWrite( left_forward_pin, 0 )
        wiringpi.digitalWrite( left_back_pin, 1 )
        wiringpi.digitalWrite( right_forward_pin, 0 )
        wiringpi.digitalWrite( right_back_pin, 1 )


th = threading.Thread(target=moter,name="th",args=())
# スレッドthの作成　targetで行いたいメソッド,nameでスレッドの名前,argsで引数を指定する
th.setDaemon(True)
# thをデーモンに設定する。メインスレッドが終了すると、デーモンスレッドは一緒に終了する
th.start()
#スレッドの開始


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

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        sys.exit()


# import threading
# import time
# import sys
# def f():
#     '''
#     非同期で行いたい処理
#     今回は一秒ごとに秒数を表示する
#     '''
#     i = 1
#     while True:
#         print(i)
#         i += 1
#         time.sleep(1)
#
# th = threading.Thread(target=f,name="th",args=())
# # スレッドthの作成　targetで行いたいメソッド,nameでスレッドの名前,argsで引数を指定する
# th.setDaemon(True)
# # thをデーモンに設定する。メインスレッドが終了すると、デーモンスレッドは一緒に終了する
# th.start()
# #スレッドの開始
#
# # 文字入力を受け付け、aだったら終了
# # メインスレッドなので、これが終了するとデーモンスレッドであるthも終了する
# while True:
#     c = sys.stdin.read(1)
#     if c == 'a':
#         sys.exit()
