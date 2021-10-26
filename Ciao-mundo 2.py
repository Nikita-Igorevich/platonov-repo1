#importing modules
import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
#defining functions
def decimal2binary(decimal):
    return[int(bit) for bit in bin(decimal)[2:].zfill(bits)]

#defining functions
def bin2dac(value):
    signal= decimal2binary(value)
    GPIO.output(dac,signal)
    return signal

#creating constants
dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 23]
troykaM=17
bits=8
levels=256
maxV=3.3

#setting GPIO modules
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)
GPIO.setup(dac, GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(leds, GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(troykaM,GPIO.OUT, initial = GPIO.HIGH)

#defining functions
def adc():
    value=0
    for steps1 in range(7 ,-1,-1):
        deltav=2**steps1
        signal=bin2dac(deltav+value)
        voltage = (deltav+value)/levels * maxV
        time.sleep(0.05)
        comopratorV = GPIO.input(4)
        if comopratorV == 1:
            value=value+deltav


    print('                                             ',value, signal, voltage)
    time.sleep(0.01)
    return value

try:
    #create variables
    measure_data = []
    value = 0

    #Fix start time
    st = time.time()


    GPIO.output(troykaM, 1)
    print("Начало измерений")
    value=adc()

   #charging capacitor
    GPIO.output(leds,decimal2binary(value))
    measure_data.append(value)
    while value <= 245:
        value1=adc()
        if value1>value:
            print("конденстатор заряжается, осталось",int((1-value1/245)*100), "%")
        value=value1
        GPIO.output(leds,decimal2binary(value))
        measure_data.append(value)
    print("Конденсатор зарядился")

    #discharging capacitor
    GPIO.output(troykaM, 0)

    while value > 1:
        value1=adc()
        if value1<value:
            print("конденстатор разряжается, осталось", int((value1/245)*100), "%")
        value = adc()
        GPIO.output(leds,decimal2binary(value))
        measure_data.append(value)

    #fix finish time and print time values
    fh = time.time()
    timem=fh-st
    deltam= timem / len(measure_data)
    fm = int(1 / deltam)
    print("Измерения завершены")
    print("Суммарное время измерений ",timem," число измерений=",len(measure_data)," частота измерений=",fm)
    mesure_str=[str(item) for item in measure_data]
    #writing in files
    with open("/home/gr104/Desktop/Scripts/platonov-repo/data.txt","w") as outfile:
        outfile.write("\n".join(mesure_str))
    with open("/home/gr104/Desktop/Scripts/platonov-repo/settings.txt","w") as outfile:
        outfile.write("Суммарное время измерений ")
        outfile.write(str(timem))
        outfile.write("\n  число измерений=")
        outfile.write(str(len(measure_data)))
        outfile.write("\n  частота измерений=")
        outfile.write(str(fm))
    plt.plot(measure_data)
    plt.show()

#executing after script
except KeyboardInterrupt:
    print("programm stopped by keyboard")
else:
    print('No exeptions')
finally:
    GPIO.output(dac, GPIO.LOW)

    GPIO.cleanup(dac)
    GPIO.cleanup(leds)
    print("end")  