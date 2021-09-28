import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(22, GPIO.IN)

def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def bin2dac(value):
    signal = decimal2binary(value)
    GP.output(dac, signal)
    return signal


dutycycle = 0

p = GPIO.PWM(3, 1000)  # channel=12 frequency=50Hz
p.start(0)
try:
    while True:
        inputStr = input("Print!")
        if inputStr.isdigit():
            value = int(inputStr)

            if value >= 100:
                print("Too big")
                continue
            elif value <= 0:
                print("what?!")
                continue
            else:
                p.start(int(inputStr))
            
        else:
            print("Enter a positive integer")
            continue
        

        
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()



