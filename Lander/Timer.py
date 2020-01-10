# CountDownTimer class
# Irv Kalb  4/16

import time

class CountUpTimer(object):
    def __init__(self):
        self.running = False
        self.savedSecondsElapsed = 0
        
    def mStart(self):
        self.secondsStart = time.time()  # get the current seconds, and save it away
        #print 'time start:', self.secondsStart
        self.running = True

    def mGetTime(self):
        if self.running:
            secondsNow = time.time()
            secondsElapsed = secondsNow - self.secondsStart
        else:
            secondsElapsed = self.savedSecondsElapsed
        return secondsElapsed

    def mGetTimeInSeconds(self):
        nSeconds = self.mGetTime()
        nSeconds = int(nSeconds)
        return nSeconds

    def mGetTimeFloat(self, nDigits=2):
        nSeconds = self.mGetTime()
        nSeconds = round(nSeconds, nDigits)
        return nSeconds
    
    def mStop(self):
        self.running = False
        secondsNow = time.time()
        self.savedSecondsElapsed = secondsNow - self.secondsStart

#############################################


class CountDownTimer(object):
    def __init__(self, nStartingSeconds):
        self.running = False
        self.secondsSavedRemaining = 0
        self.nStartingSeconds = nStartingSeconds
        
    def mStart(self):
        secondsNow = time.time()  
        self.secondsEnd = secondsNow + self.nStartingSeconds 
        self.running = True

    def mGetTime(self):
        if self.running:
            secondsNow = time.time()
            secondsRemaining = self.secondsEnd - secondsNow
        else:
            secondsRemaining = self.secondsSavedRemaining
        return secondsRemaining

    def mGetTimeInSeconds(self):
        nSeconds = self.mGetTime()
        nSeconds = int(nSeconds)
        return nSeconds

    
    def mStop(self):
        self.running = False
        secondsNow = time.time()
        self.secondsSavedRemaining = self.secondsEnd - secondsNow
