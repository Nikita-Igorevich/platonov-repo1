import RPi.GPIO as GPIO
import time

def dectobin(v, r):
    return [int(bit) for bit in bin(v)[2:].zfill(r)]

def bintodec(binn):
    summ = 0
    bin_t = binn[::-1]
    for i in range(len(bin_t)):
        summ = summ + (2**i)*bin_t[i]
    return summ

def dectodtac(v,r,dac):
    sig = dectobin(v,r)
    GPIO.output(dac, sig)
    time.sleep(0.1)
    return sig

def dtacout(dac, sig,ti):
    GPIO.output(dac, sig)
    time.sleep(ti)
    
def ledsindic(leds, sig):
    s = [0 for el in sig]
    check = False
    d = bintodec(sig)
    a = round(8*d/256)
    for i in range(len(s)):
        if i<= a:
            s[i]=1
    
    GPIO.output(leds,s)

def atdc(dac, comp, t):
    dig = [ 0 for _ in dac ]
    for i in range(len(dac)):
        dig[i] = 1
        dtacout(dac, dig, t)
        if GPIO.input(comp):
            dig[i] = 1
        else:
            dig[i] = 0
    return dig
        
    
def atdc2(dac,comp,t):
    for i in range(256):
        sig = dectobin(i, 8)
        dtacout(dac, sig, t)
        if (GPIO.input(comp)) == 0:
            return sig
    return sig
    
    
    
leds =  [ 21, 20, 16, 12, 7, 8, 25, 24 ]

dac  =  [ 26, 19, 13, 6, 5, 11, 9, 10 ]

aux  =  [ 22, 23, 27, 18, 15, 14, 3, 2 ]

trModV = 17

comp = 4
 
mV = 3.3
bits = len(dac)
raz = 2**bits

GPIO.setmode(GPIO.BCM)


GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)

GPIO.setup(leds, GPIO.OUT, initial = GPIO.LOW)


GPIO.setup(trModV, GPIO.OUT, initial = GPIO.HIGH)


GPIO.setup(comp, GPIO.IN)



try:
    check = 0
    while 0==0:
        t = 0.05
        if check == 0:
            print('Do you want to start? Type y for yes and  for n')
            inputS = input()
            if inputS == 'y':
                check = 1
                #digital = atdc(dac, comp, t)
                digital = atdc2(dac, comp, t)
                print('digital signal', ' '.join(map(str, digital)))
                print('decimal', bintodec(digital))
                volt = ( bintodec(digital) / raz ) * mV
                
                
            elif inputS == 'n':
                break
        if check:
            ledsindic(leds, digital)
            #digital = atdc(dac, comp, t)
            digital = atdc2(dac, comp, t)
            print('digital signal', ' '.join(map(str, digital)))
            print('decimal', bintodec(digital))
            volt = ( bintodec(digital) / raz ) * mV
            #print('approximate voltage', volt)
            GPIO.output(dac, GPIO.LOW)
        else:
            print('Incorrect input, please try again.')
            
except KeyboardInterrupt:
    print("Program was interupted from keyboard")
    
else:
    print("No exceptions happened")
    
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(leds, GPIO.LOW)
    GPIO.cleanup(dac)
    GPIO.cleanup(leds)
    GPIO.cleanup(trModV)
    GPIO.cleanup(comp)
    print("Done, GPIO cleaned up")