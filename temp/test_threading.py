import threading
import time
import sys
def f():
    '''
    非同期で行いたい処理
    今回は一秒ごとに秒数を表示する
    '''
    i = 1
    while True:
        print(i)
        i += 1
        time.sleep(1)

th = threading.Thread(target=f,name="th",args=())
# スレッドthの作成　targetで行いたいメソッド,nameでスレッドの名前,argsで引数を指定する
th.setDaemon(True)
# thをデーモンに設定する。メインスレッドが終了すると、デーモンスレッドは一緒に終了する
th.start()
#スレッドの開始

# 文字入力を受け付け、aだったら終了
# メインスレッドなので、これが終了するとデーモンスレッドであるthも終了する
while True:
    c = sys.stdin.read(1)
    if c == 'a':
        sys.exit()
