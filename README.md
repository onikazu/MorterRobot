# MorterRobot
## 概要
４つのタイヤが付いたカメラ付き車型ロボット

## 使い方・プログラムの説明
- test.py
一つのモーターを操作するプログラム
test_circuit.JPGのように回路を組み、一つのモータにつなげる。
命令はコマンド引数を用いる
第一引数でgo(順回転)、back(逆回転)といった命令。
第二引数で命令の実行時間を指定する事ができる。

~~~
# 実行例
python3 test.py go 5
~~~


- double_test.py
２つのモータを同時に操作するプログラム
https://qiita.com/imcuddles/items/c05cbea95db1f7469fed
にあるように回路をつなぐ

~~~
# 実行例
python3 double_test.py gostraight 5
~~~

- motor_and_print.py
一つのモーターを動かしながらカウントを印字するプログラム。モーターは１０秒後に停止する。
test_circuit.JPGのように回路を組み、一つのモータにつなげる。
命令はコマンド引数を用いる
第一引数でgo(順回転)、back(逆回転)といった命令。

~~~
# 実行例
python3 motor_and_print.py go 5
~~~

- motor_and_camera.py
一つのモーターを動かしながらカメラを同時に操作するプログラム。
test_circuit.JPGのように回路を組み、一つのモータにつなげる。
命令はコマンド引数を用いる
第一引数でgo(順回転)、back(逆回転)といった命令。

~~~
# 実行例
python3 motor_and_camera.py go
~~~

- motor_and_modelcamera.py
一つのモーターを動かしながら物体認識をするカメラを同時に操作するプログラム。
test_circuit.JPGのように回路を組み、一つのモータにつなげる。
命令はコマンド引数を用いる
第一引数でgo(順回転)、back(逆回転)といった命令。

~~~
# 実行例
python3 motor_and_modelcamera.py go
~~~

- motor_modelstopper.py
一つのモーターを動かしながら物体認識をするカメラを同時に操作し「notebook」が写ったらモーターを停止するプログラム。
test_circuit.JPGのように回路を組み、一つのモータにつなげる。
命令はコマンド引数を用いる
第一引数でgo(順回転)、back(逆回転)といった命令。

~~~
# 実行例
python3 motor_modelstopper.py go
~~~

- double_motor_modelstopper.py
２つのモーターを動かしながら物体認識をするカメラを同時に操作し「notebook」が写ったらモーターを停止するプログラム。
https://qiita.com/imcuddles/items/c05cbea95db1f7469fed
にあるように回路をつなぐ
命令はコマンド引数を用いる。
第一引数でgostraight(直進)、goright(右折)といった命令。




## 参考資料
wiringpi のインストール
https://qiita.com/nanbuwks/items/9f7e709025b587c038d2

ta7291pのピンについて
http://d.hatena.ne.jp/seinzumtode/20120724/1343116830

raspberry pi3 modelb のピンについて
https://pc.watch.impress.co.jp/docs/column/nishikawa/1006048.html

配線、test.pyについて
https://qiita.com/RyosukeKamei/items/147de58738084826f749
http://kaiware007.hatenablog.jp/entry/2015/07/07/024930

配線、double_test.pyについて
https://qiita.com/imcuddles/items/c05cbea95db1f7469fed