import wiringpi
import time
import sys
# 並列処理のためのライブラリ
import threading
# スレッド間での変数のやり取りに必要
from threading import Value


def move(order):
    second = 3
    if order == "goright":
        wiringpi.digitalWrite( right_forward_pin, 1 )
        wiringpi.digitalWrite( right_back_pin, 0 )
        time.sleep(second)
    elif order == "backright":
        wiringpi.digitalWrite( right_forward_pin, 0 )
        wiringpi.digitalWrite( right_back_pin, 1 )
        time.sleep(second)
    elif order == "goleft":
        wiringpi.digitalWrite( left_forward_pin, 1 )
        wiringpi.digitalWrite( left_back_pin, 0 )
        time.sleep(second)
    elif order == "backleft":
        wiringpi.digitalWrite( left_forward_pin, 0 )
        wiringpi.digitalWrite( left_back_pin, 1 )
        time.sleep(second)
    elif order == "gostraight":
        wiringpi.digitalWrite( left_forward_pin, 1 )
        wiringpi.digitalWrite( left_back_pin, 0 )
        wiringpi.digitalWrite( right_forward_pin, 1 )
        wiringpi.digitalWrite( right_back_pin, 0 )
        time.sleep(second)
    elif order == "back":
        wiringpi.digitalWrite( left_forward_pin, 0 )
        wiringpi.digitalWrite( left_back_pin, 1 )
        wiringpi.digitalWrite( right_forward_pin, 0 )
        wiringpi.digitalWrite( right_back_pin, 1 )
        time.sleep(second)


    # 第2引数が0の場合は、ブレーキをしない
    # 第1引数がbreakの場合は、ブレーキ

    print("ブレーキ！")
    wiringpi.digitalWrite( right_forward_pin, 1 )
    wiringpi.digitalWrite( left_forward_pin, 1 )
    wiringpi.digitalWrite( right_back_pin, 1 )
    wiringpi.digitalWrite( left_back_pin, 1 )


def say_goodbye():
    while True:
        print("Good bye!")

def say_hello(situation, who):
    while True:
        print("Good {} {} !".format(situation, who))

if __name__ == '__main__':
# ------------------------------------------
    # 引数
    param = sys.argv

    # 第1引数
    # go : 回転
    # back : 逆回転
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
    who = "kazuki"
# ------------------------------------

# ------------------------------------

    th1 = threading.Thread(target=say_hello, name='morning_thread', args=('morning', who))
    th2 = threading.Thread(target=say_hello, name='eveningthread', args=('evening', who))
    th3 = threading.Thread(target=say_goodbye, name='byethread')
    th4 = threading.Thread(target=move, name='morterthread',args=(order,))
    th1.start()
    th2.start()
    th3.start()
    th4.start()
