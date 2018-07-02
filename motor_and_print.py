"""
１０秒カウントし、１０秒間だけモーターを動かすプログラム
→　成功

"""

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


def loop_print():
    count = 0
    while True:
        print(count)
        count += 1
        time.sleep(1)


if __name__ == "__main__":
    param = sys.argv
    order = param[1]
    motor1_pin = 23
    motor2_pin = 24

    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(motor1_pin, 1)
    wiringpi.pinMode(motor2_pin, 1)

    th1 = threading.Thread(target=motor, name="motor", args=())
    th2 = threading.Thread(target=loop_print, name="loop_print", args=())

    th1.start()
    th2.start()