'''
Created on Aug 6, 2014

@author: johannes
uses
https://github.com/sarfata/pi-blaster/

'''
#import RPi.GPIO as GPIO
import threading
import time
import wiringpi2 as led

class LedDriver(object):

    def __init__(self):
        led.wiringPiSetupGpio()
        led.pinMode(18, 2)      # sets GPIO 24 to output

        #self.pwmLed=pwmLed
        
        #self.ledPin=18
        self.pwmThread=threading.Thread(target=self.fade)

    def fadeUp(self):
        self.pwmThread=threading.Thread(target=self.fade,args=(0,))
        self.pwmThread.daemon=True
        self.pwmThread.start()

    def fadeDown(self):
        self.pwmThread=threading.Thread(target=self.fade,args=(1,))
        self.pwmThread.daemon=True
        self.pwmThread.start()
    
    def fade(self,direction):
        if direction:
            for i in range(1000,-1,-1):
                #self.pwmLed.ChangeDutyCycle(i)
                led.pwmWrite(18,i)
                time.sleep(0.005)
        else:
            for i in range(0,1001,1):
                #self.pwmLed.ChangeDutyCycle(i)
                led.pwmWrite(18,i)
                time.sleep(0.005)

def main():
    print "does not work"
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(18,GPIO.OUT)
    
    pwmLed=GPIO.PWM(18,2000)
    q1=Queue.Queue()
    q1.put("")
    q2=Queue.Queue()
    q2.put("")
    ledDriver=LedDriver(pwmLed,q1,q2)
    ledDriver.fadeUp()
    time.sleep(10)
    tmp=q1.get()
    tmp=q2.get()
    print"removed objects"
    time.sleep(5)
    print "finnished"

if __name__ == '__main__':
    main()

        
        