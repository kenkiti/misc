#! -*- coding: cp932 -*-
import sys, time, threading

class myThread(threading.Thread):
    alive = True
    def run(self):
        while self.alive:
            sys.stdout.write('.')
            time.sleep(1)
    def kill(self):
        self.alive = False

def sandglass(func):
    """時間経過を表示させるデコレータ
    """
    def wrapper(*args, **keys):
        try:
            t = myThread()
            #print '開始',
            t.start()
            ret = func(* args, **keys)
            return ret
        finally:
            t.kill()
            #print '終了'

    return wrapper

if __name__ == "__main__":

    @sandglass
    def do_something():
        """何か時間のかかる処理。
        """
        time.sleep(10) 

    print '開始',
    do_something()
    print '終了'
