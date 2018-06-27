import threading, time, datetime

g_cnt = 0

class MyThread1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "MyThread1"

    def run(self):
        global g_cnt

        while True:        
            # read
            print('{0} :value -> {1} :time -> {2}'.format(self.name, str(g_cnt), str(datetime.datetime.now())))
            time.sleep(5)

            # write
            g_cnt = g_cnt + 5
            print('{0} :value -> {1} :time -> {2}'.format(self.name, str(g_cnt), str(datetime.datetime.now())))

class MyThread2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "MyThread2"

    def run(self):
        global g_cnt

        while True:
            # read
            print('{0} :value -> {1} :time -> {2}'.format(self.name, str(g_cnt), str(datetime.datetime.now())))

            time.sleep(10)

            # write
            g_cnt = g_cnt + 10
            print('{0} :value -> {1} :time -> {2}'.format(self.name, str(g_cnt), str(datetime.datetime.now())))

thread1 = MyThread1()
thread2 = MyThread2()

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print('Result :value -> {0} :time -> {1}'.format(str(g_cnt), str(datetime.datetime.now())))
