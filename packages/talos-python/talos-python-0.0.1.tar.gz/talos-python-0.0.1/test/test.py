#
# Copyright 2020, Xiaomi.
# All rights reserved.
# Author: huyumei@xiaomi.com
# 
 
import time
import threading

balance = 0

def run_thread1():
    while True:
        print("1")


def run_thread2():
    while True:
        print("2")


t1 = threading.Thread(target=run_thread1)
t2 = threading.Thread(target=run_thread2)
t1.start()
time.sleep(5)
t2.start()
t1.join()
t2.join()
print(balance)