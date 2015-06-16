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
    """���Ԍo�߂�\��������f�R���[�^
    """
    def wrapper(*args, **keys):
        try:
            t = myThread()
            #print '�J�n',
            t.start()
            ret = func(* args, **keys)
            return ret
        finally:
            t.kill()
            #print '�I��'

    return wrapper

if __name__ == "__main__":

    @sandglass
    def do_something():
        """�������Ԃ̂����鏈���B
        """
        time.sleep(10) 

    print '�J�n',
    do_something()
    print '�I��'
