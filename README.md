# MorterRobot
## 概要
４つのタイヤが付いたカメラ付き車型ロボット（未完）

## 使い方
- test.py
test_circuit.JPGのように回路を組み、一つのモータにつなげる。
命令はコマンド引数を用いる
第一引数でgo(順回転)、back(逆回転)といった命令。
第二引数で命令の実行時間を指定する事ができる。

~~~
# 実行例
python3 test.py go 5
~~~


- double_test.py  
.JPGのようにきろ

- robot_with_camera.py  
命令はコマンド引数を用いる
第一引数でdouble_test.pyと同じように命令できる
notebook が映ると止まる

~~~
# 実行例
python3 robot_with_camera.py go
~~~


## 参考資料
