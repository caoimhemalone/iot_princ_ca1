import math
import fcntl, socket, struct, dweepy, time, platform, random
from grovepi import *

dht_sensor_port = 7
led = 4
button = 3

def getTemp():
    try:
        [temp, hum] = dht(dht_sensor_port, 0)
        print "temp =", temp,
        if math.isnan(temp):
            temp = 0
        return float(temp)
    except (IOError, TypeError) as e:
        print "Error"

def getHumidity():
    try:
        [temp, hum] = dht(dht_sensor_port, 0)
        print "humidity =", hum, "%"
        if math.isnan(hum):
            hum =0
        return hum
    except (IOError, TypeError) as e:
        print "Error"

def getLED():
    try:
        button_status = digitalRead(button)
        if button_status:
            digitalWrite(led,1)
            print ("LED ON")
            return 1
        else:
            digitalWrite(led,0)
            print("LED OFF")
            return 0
    except (IOError, TypeError) as e:
        print ("Error")

def getOS():
    return platform.platform()

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0X8927, struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])

def post(dic):
    thing = 'Caoimhe Malone'
    print dweepy.dweet_for(thing, dic)

def getReadings():
    dict = {}
    dict ["led"] = getLED()
    dict ["temperature"] = getTemp()
    dict ["humidity"] = getHumidity()
    dict ["mac-address"] = getHwAddr('eth0')
    dict ["operating system"] = getOS()
    return dict

while True:
    dict = getReadings();
    post(dict)
    time.sleep(5)


