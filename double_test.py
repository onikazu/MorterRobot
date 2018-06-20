# GPIOを制御するライブラリ
import wiringpi
# タイマーのライブラリ
import time
# 引数取得
import sys

# 引数
param = sys.argv

# 第1引数
# go : 回転
# back : 逆回転
# break : ブレーキ
order = param[1]

# 第2引数 秒数
second = int(param[2])

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

if order == "goright":
    if second == 0:
        print("右前進 止めるときはbreak 0コマンド！")
    else:
        print(str(second)+"秒右前進")
    wiringpi.digitalWrite( right_forward_pin, 1 )
    wiringpi.digitalWrite( right_back_pin, 0 )
    time.sleep(second)
elif order == "backright":
    if second == 0:
        print("右後進 止めるときはbreak 0コマンド！")
    else:
        print(str(second)+"秒右後進")    
    wiringpi.digitalWrite( right_forward_pin, 0 )
    wiringpi.digitalWrite( right_back_pin, 1 )
    time.sleep(second)
elif order == "goleft":
    if second == 0:
        print("左前進 止めるときはbreak 0コマンド！")
    else:
        print(str(second)+"秒左前進")    
    wiringpi.digitalWrite( left_forward_pin, 1 )
    wiringpi.digitalWrite( left_back_pin, 0 )
    time.sleep(second)
elif order == "backleft":
    if second == 0:
        print("左後進 止めるときはbreak 0コマンド！")
    else:
        print(str(second)+"秒左後進")    
    wiringpi.digitalWrite( left_forward_pin, 0 )
    wiringpi.digitalWrite( left_back_pin, 1 )
    time.sleep(second)
elif order == "gostraight":
    if second == 0:
        print("前進 止めるときはbreak 0コマンド！")
    else:
        print(str(second)+"秒前進")    
    wiringpi.digitalWrite( left_forward_pin, 1 )
    wiringpi.digitalWrite( left_back_pin, 0 )
    wiringpi.digitalWrite( right_forward_pin, 1 )
    wiringpi.digitalWrite( right_back_pin, 0 )
    time.sleep(second)
elif order == "back":
    if second == 0:
        print("後進 止めるときはbreak 0コマンド！")
    else:
        print(str(second)+"秒後進")
    wiringpi.digitalWrite( left_forward_pin, 0 )
    wiringpi.digitalWrite( left_back_pin, 1 )
    wiringpi.digitalWrite( right_forward_pin, 0 )
    wiringpi.digitalWrite( right_back_pin, 1 )
    time.sleep(second)
        
    
# 第2引数が0の場合は、ブレーキをしない
# 第1引数がbreakの場合は、ブレーキ
if order == "break" or second != 0:
    print("ブレーキ！")
    wiringpi.digitalWrite( right_forward_pin, 1 )
    wiringpi.digitalWrite( left_forward_pin, 1 )
    wiringpi.digitalWrite( right_back_pin, 1 )
    wiringpi.digitalWrite( left_back_pin, 1 )
