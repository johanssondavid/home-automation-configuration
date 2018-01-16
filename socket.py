import time
import sys
import RPi.GPIO as GPIO

import os
import fcntl

class Lock:
  def __init__(self, filename):
    self.filename = filename
    # This will create it if it does not exist already
    self.handle = open(filename, 'w')
                                   
  # Bitwise OR fcntl.LOCK_NB if you need a non-blocking lock 
  def acquire(self):
    fcntl.flock(self.handle, fcntl.LOCK_EX)
                                                                 
  def release(self):
    fcntl.flock(self.handle, fcntl.LOCK_UN)
                                                                                            
  def __del__(self):
    self.handle.close()


#       HHHH HHHH HHHH HHHH HHHH HHHH HHGO CCEE
a_on  = '1010100101101001010101100101011001010101010101010110100101010101'
a_off = '1010100101101001010101100101011001010101010101010110101001010101'
b_on  = '1010100101101001010101100101011001010101010101010110100101010110'
b_off = '1010100101101001010101100101011001010101010101010110101001010110'
c_on  = '1010100101101001010101100101011001010101010101010110100101011001'
c_off = '1010100101101001010101100101011001010101010101010110101001011001'
d_on  = '1010100101101001010101100101011001010101010101010110100101011010'
d_off = '1010100101101001010101100101011001010101010101010110101001011010'

e_on  = '1010100101101001010101100101011001010101010101010110100101101010'
e_off = '1010100101101001010101100101011001010101010101010110101001101010'
f_on  = '1010100101101001010101100101011001010101010101010110100101100110'
f_off = '1010100101101001010101100101011001010101010101010110101001100110'
g_on  = '1010100101101001010101100101011001010101010101010110100101101001'
g_off = '1010100101101001010101100101011001010101010101010110101001101001'
h_on  = '1010100101101001010101100101011001010101010101010110100101101001'
h_off = '1010100101101001010101100101011001010101010101010110101001101001'

short_delay = 0.00025
long_delay  = 0.00125
sync_delay  = 0.00250
pause_delay = 0.01000


NUM_ATTEMPTS = 10
TRANSMIT_PIN = 24

def delay(s):
    ms = s * 1000
    end = time.time() * 1000 + ms
    while time.time() * 1000 < end:
        continue

def transmit_code(code):
    '''Transmit a chosen code string using the GPIO transmitter'''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    for t in range(NUM_ATTEMPTS):

        # sync
        GPIO.output(TRANSMIT_PIN, 1)
        delay(short_delay)
        GPIO.output(TRANSMIT_PIN, 0)
        delay(sync_delay)

        for i in code:
            if i == '1':
                GPIO.output(TRANSMIT_PIN, 1)
                delay(short_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                delay(short_delay)
            elif i == '0':
                GPIO.output(TRANSMIT_PIN, 1)
                delay(short_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                delay(long_delay)
            else:
                continue

        # pause
        GPIO.output(TRANSMIT_PIN, 1)
        delay(short_delay)
        GPIO.output(TRANSMIT_PIN, 0)
        delay(pause_delay)

    GPIO.cleanup()

    delay(1)

if __name__ == '__main__':
    for argument in sys.argv[1:]:
        try:
            lock = Lock("/tmp/socket.lock")
            lock.acquire()
            exec('transmit_code(' + str(argument) + ')')
        finally:
            lock.release()

