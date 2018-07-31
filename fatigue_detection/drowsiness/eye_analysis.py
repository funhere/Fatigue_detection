# -*- coding: utf-8 -*-
import numpy as np
import cv2

from driver_tracking.utils.ring_buffer import RingBuffer
from driver_tracking.logging.log_data import LogData
#from driver_tracking.drowsiness.drowsiness import Drowsiness
from driver_tracking.video.frame_series import FrameSeries

EYE_AR_THRESHOLD = 0.3
MAX_RB_EYES = 50
MAX_RB_BLINKS = 150
EYE_OPEN = 0
EYE_CLOSE = 1
SHOW_PERIOD = 100 
EYE_CLOSED_RATE = 0.8 
EYE_BLINK_THRESH = 7 

class EyeAnalyzer():
	
    def __init__(self):
        self.isEyeBlinked = False
        self.isEyeClosed = False
        self.lastState = EYE_OPEN
        self.currState = EYE_OPEN
        self.showBlink = 0
        self.RB_eyes = RingBuffer(MAX_RB_EYES)
        self.RB_blinks = RingBuffer(MAX_RB_BLINKS)
        self.blinkRate = 0
        self.eyeClosedRate = 0

        # initialize ring buffer
        for _ in range(0,self.RB_eyes.getSize()):
            self.RB_eyes.append(False)
        for _ in range(0,self.RB_blinks.getSize()):
            self.RB_blinks.append(False)
        
    def do_analysis(self,FrameSeries):
        self.clear_status()
        self.get_eyes_status(FrameSeries)
        self.get_log_values()
        
	
    def clear_status(self):
        self.isEyeBlinked = False
        self.isEyeClosed = False
        
    def update_status(self,FrameSeries):
        return FrameSeries.detected()
    
   
    def set_frame(self,frame):
        #self.orgFrame = frame.copy()
        self.orgFrame = frame
        
    def get_frame():
        return self.orgFrame
    
    def set_iFrame(self,i_frame):
        self.i_frame = i_frame
        
    def get_iFrame():
        return self.i_frame
        
        
    def get_eyes_status(self,FrameSeries):
        i = 0
        eye_close_count = 0
        eye_blink_count = 0
        
        #blinking and closing detection
        if self.update_status(FrameSeries): 
            self.isEyeClosed = True
            self.currState = EYE_CLOSE
        else:
            self.isEyeClosed = False
            self.currState = EYE_OPEN

        if self.currState == EYE_OPEN and self.lastState == EYE_CLOSE:
            self.isEyeBlinked = True
            self.showBlink = SHOW_PERIOD
        else:
            self.isEyeBlinked = False
            
        self.lastState = self.currState   
        if self.showBlink > 0:
            #cv2.putText(self.orgFrame, "Eye blinks: {}".format(self.blinkRate), (250, 60),
            #cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            #logger.add_frame_log_data([LogData(['blinks', 'series'], 1, self.orgFrame)])
            
            self.showBlink -= 1
           
        #Ring buffers
        self.RB_eyes.append(self.isEyeClosed)
        self.RB_blinks.append(self.isEyeBlinked)
        
        #Sleep statistic
        count = 0
        rb_eye = self.RB_eyes  #ring buffer of eyes closed counter
        if (len(rb_eye.get()) == rb_eye.getSize()) :
            for x in rb_eye.get() :
                count += 1
                if x == True and count < rb_eye.getSize() :
                    eye_close_count += 1
             
            self.eyeClosedRate = eye_close_count/rb_eye.getSize() *100   
            if(eye_close_count >= (rb_eye.getSize() * EYE_CLOSED_RATE) ) :
                cv2.putText(self.orgFrame, "SLEEPING ALERT! EyeClosedRate: {0}/100".format(self.eyeClosedRate), (10, 230),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)        
    
    
        #Blinking statistic
        b_count = 0
        rb_blink = self.RB_blinks
        if(len(rb_blink.get()) == rb_blink.getSize()):
            for x in rb_blink.get():
                b_count += 1
                if x == True and b_count < rb_blink.getSize():
                    eye_blink_count += 1 
                    
            self.blinkRate = eye_blink_count       
            if(self.blinkRate >= EYE_BLINK_THRESH) :
                cv2.putText(self.orgFrame, "Blinks ALERT! BlinkRate = {0}/{1} frame ".format(self.blinkRate,MAX_RB_BLINKS), (10, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)     
            else:
                cv2.putText(self.orgFrame, "BlinkRate = {0}/{1} frame ".format(self.blinkRate,MAX_RB_BLINKS), (230, 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2) 


    def get_log_values(self):
        return [

			LogData(['drowsiness', 'BlinkRate'], self.blinkRate, self.i_frame),
			LogData(['drowsiness', 'EyeClosedRate'], self.eyeClosedRate, self.i_frame),

		]

