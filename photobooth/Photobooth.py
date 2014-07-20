#!/usr/bin/env python

'''
Created on Mar 19, 2014

@author: johannes
'''
from Modules.Camera import Camera
from Modules.Twitter import Twitter
from Modules.Facebook import Facebook
from Modules.ImageProcessor import ImageProcessor
from Modules.SimpleThermalPrinter import SimpleThermalPrinter
from Modules.Picamera import Picamera
import Queue
import json,time,threading, sys, select
import datetime
import RPi.GPIO as GPIO


'''
todo 
make a picture queue where the camera puts its images and the qr code
put the camera in its own thread

make the printer  thread
let the printer run with a fifo where it takes images and prints them when some appears

'''

class Photobooth(object):
    '''
    classdocs
    '''

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
        '''
        Constructor
        '''
        #config=dict()
        #with open('apiconfigs.txt', 'rb') as fp:
            #config = json.load(fp)
        #self.twitter=Twitter(config["twitter"])
        #self.facebook=Facebook(config["facebook"])
        #self.printer=Printer()
        #self.uploader=UploadServer()

        self.cameraToRasterQueue = Queue.Queue()
        self.rasterToPrinterQueue = Queue.Queue()
        self.quitEvent = threading.Event()
        print "made events and queues"
        
        print "init imageprocessor"
        self.imageProcessor=ImageProcessor(self.quitEvent,self.cameraToRasterQueue,self.rasterToPrinterQueue)
        print "init picamera"
        self.picamera=Picamera(self.quitEvent,self.cameraToRasterQueue)
        print "init printer"
        self.printer=SimpleThermalPrinter(self.quitEvent,self.rasterToPrinterQueue)
        
        '''state thread'''

    def startShoot(self):
        if not self.picamera.isCaptureThreadRunning() and self.cameraToRasterQueue.empty() and self.rasterToPrinterQueue.empty():
            print "now shooting"
            self.shoot()
        else:
            print("busy shooting")
        
    def stopShoot(self):
        self.quitEvent.set()
        self.cameraToRasterQueue.put(None)
        self.rasterToPrinterQueue.put(None)
        #self.stateThread.join()

    def shoot(self):
        print "shooting"
        self.picamera.captureFourImagesThreaded()
        print "told camera to shoot"
        #facebookImageAndString=self.imageProcessor.composeForFacebook(dir)
        #twitterImageAndString=self.imageProcessor.composeForTwitter(dir)
        
        #dateString=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
        
        '''token=self.imageProcessor.saveImageToOutgoing(
                           dateString,
                           [
                            facebookImageAndString,
                            twitterImageAndString
                            ],dir)
                        '''
        #pixels=self.imageProcessor.composeForPrinterReturnPixelArrays(dir,2)
        #for pixelarray in pixels:
         #   self.printer.printPixelArray(pixelarray)
        
        
        '''chdk shooting and downloading'''
        #photoDir=self.camera.captureReturnDir()
        #message="Testing "+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        
        '''make photoframe'''
        
        '''upload two first images to twitter'''
        #imagePath=self.image_processor.composeForTwitter(photoDir)
        #self.twitter.uploadImage(message,imagePath)
        
        #imagePath=self.image_processor.composeForFacebook(photoDir)
        #self.facebook.uploadImage(message,imagePath)
        
        '''make photostrip'''
       # image_paths=self.image_processor.composeForPrinter(photoDir)
        
        '''print photos'''
        #self.printer.printPhotoStrip(image_paths)
        print "press s to shoot"

        
def main():
    photobooth=Photobooth()
    print("press s to shoot")
    
    try:
        while True:
            time.sleep(0.2)
            if(GPIO.input(4)==0):
                time.sleep(0.2)
                if(GPIO.input(4)==0):
                    photobooth.startShoot()
        #    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
         #       c = sys.stdin.readline()
          #      c=c[0:1]
           #     if(c=='s'): 
            #        photobooth.startShoot()
    except KeyboardInterrupt:
        print("exiting")
        photobooth.stopShoot()
        GPIO.cleanup()
if __name__ == '__main__':
    main()