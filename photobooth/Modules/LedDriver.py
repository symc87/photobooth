'''
Created on Aug 6, 2014

@author: johannes
uses
https://github.com/sarfata/pi-blaster/

'''
import RPi.GPIO as GPIO
import threading
import time
import Queue

class LedDriver(object):

    def __init__(self,q1,q2):
        self.q1=q1
        self.q2=q2
        self.ledPin=18
        self.pwmThread=threading.Thread(target=self.fade)

    def fadeUp(self):
        self.pwmThread=threading.Thread(target=self.fade)
        #self.pwmThread.daemon=True
        self.pwmThread.start()
    
    def fade(self):
        print "opening piblaster in thread"
        blaster_file = open("/dev/pi-blaster", "a")
        for i in range(0,100,1):
            blaster_file.write("%d=%d\n"%(self.ledPin,i))
            time.sleep(0.2)
        time.sleep(1)
        print "faded up"
        while(not self.q1.empty() and not self.q2.empty()):
            time.sleep(0.1)
        for i in range(100,0,-1):
            string="%d=%d\n"%(self.ledPin,i)
            blaster_file.write(string)
            time.sleep(0.2)
        print "faded down"
        blaster_file.close()


def main():
    q1=Queue.Queue()
    q1.put("")
    q2=Queue.Queue()
    q2.put("")
    ledDriver=LedDriver(q1,q2)
    ledDriver.fadeUp()
    time.sleep(5)
    tmp=q1.get()
    tmp=q2.get()
    time.sleep(5)
    print "finnished"

if __name__ == '__main__':
    main()

        
        