import RPi.GPIO as GPIO
import time
import multiprocessing

global danger_state
#danger_state=False


#Declairing the pins
Serialclock = 12
Masterout = 6
Masterin = 5
Chipselect = 4
mq9_dpin = 13
mq9_apin = 0


def init():
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Serialclock, GPIO.OUT)
    GPIO.setup(Masterout, GPIO.IN)
    GPIO.setup(Masterin, GPIO.OUT)
    GPIO.setup(Chipselect, GPIO.OUT)
    GPIO.setup(mq9_dpin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
def Calibration():
    SensorValue = 0
    #print("SensorValue = {}".format(readadc(mq9_apin, Serialclock, Masterin, Masterout, Chipselect)))
    for i in range(100):
        SensorValue = SensorValue + readadc(mq9_apin, Serialclock, Masterin, Masterout, Chipselect)

    SensorValue = SensorValue / 100
    #print("SensorValue = {}".format(SensorValue))
    SensorVolt = (SensorValue / 1024) * 5
    #print("SensorVolt = {}".format(SensorVolt))
    RS_Air = (5 - SensorVolt) / SensorVolt
    R0 = RS_Air / 9.9
    return R0
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if((adcnum > 7) or (adcnum < 0)):
        return -1
    GPIO.output(cspin, True)
    GPIO.output(clockpin, False)
    GPIO.output(cspin, False)

    commandout = adcnum
    commandout |= 0x18
    commandout <<= 3
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)

        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)

    adcout = 0
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if GPIO.input(misopin):
            adcout |= 0x1

    GPIO.output(cspin, True)
    adcout >>= 1
    return adcout

def start_output():
    global explosive_gas_value
    SensorValue = readadc(mq9_apin, Serialclock, Masterin, Masterout, Chipselect)
    SensorVolt = (SensorValue / 1024) * 5
    RS_Gas = (5 - SensorVolt) / SensorVolt
    Ratio = RS_Gas / R0
    #print("Current gas AD value = "+str("%.2f"%(SensorValue)))
    #print("Ratio = {}".format(Ratio))
    explosive_gas_value=(1000*(Ratio)**(-2.24))
    print("Current LPG: {} ppm".format(1000*(Ratio)**(-2.24) ))
    time.sleep(0.5)

def output():
    SensorValue = readadc(mq9_apin, Serialclock, Masterin, Masterout, Chipselect)
    SensorVolt = (SensorValue / 1024) * 5
    RS_Gas = (5 - SensorVolt) / SensorVolt
    Ratio = RS_Gas / R0
    #print("Current gas AD value = "+str("%.2f"%(SensorValue)))
    #print("Ratio = {}".format(Ratio))
    explosive_gas_value=(1000*(Ratio)**(-2.24))
    print("Current LPG: {} ppm".format(1000*(Ratio)**(-2.24) ))
    #print("Current LPG: {} ppm".format(explosive_gas_value))
    f = open('DS.txt', 'r+')
    f.truncate(15)
    if (explosive_gas_value < float(75)):
        f.write("False")
    if (explosive_gas_value > float(75)):
        f.write("True")
    f.close()
    time.sleep(0.5)
    output()
        

     
      
def gas_main():
    init()
    global R0
    R0 = Calibration()
    start_output()




    
        







