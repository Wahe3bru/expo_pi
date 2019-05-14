"""
MJRoBot IoT Local Weather Station
Sensor Data - Station:
    Temperature: External (not physicaly at station)
    Temperature: Station
    Humidity: Station
    Pressure: (Sea Level) 
    Altitude (calculated due absolut atmosferic pression)
Real Altitude: Station  ==> 950m (Lo Barnechea, Chile)
All local data uploaded to ThingSpeak.com
Channel Id: 483033
Client library for the thingspeak.com API developed by Mikolaj Chwaliz and Keith Ellis.
The library can be download from: https://github.com/mchwalisz/thingspeak
Install using: pip install thingspeak
Code developed by Marcelo Rovai - MJRoBot.org @ 26April18
"""
#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from datetime import datetime
import urllib2
# Client library for the thingspeak.com API 
#import thingspeak  


# ThingSpeak channel credentials 
chId = 765856
tsKey='2I679FNJD20ZWWG8'
tsUrl='https://api.thingspeak.com/update'
#ts = thingspeak.Channel(chId, tsUrl ,tsKey)

#GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

PIN_TRIGGER = 7
PIN_ECHO = 11

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

GPIO.output(PIN_TRIGGER, GPIO.LOW)

REST_API_URL = "https://api.powerbi.com/beta/efdf19a6-7ca0-43bd-b3aa-f960679015b0/datasets/2b3ea02e-c380-4abe-86b9-609d02a584b3/rows?key=ZZAAtO0VQVXsuDvtquu8E2zknyQKQykcOaRnkPO9iL3yUAXxmIZEDv8UBbcTfHhs3XzMfWhTtV%2BnDaY6g3aPCA%3D%3D"
#Get Distance
def getDist():
    global distance
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(PIN_TRIGGER,GPIO.LOW)

    while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time

    distance = round(pulse_duration * 17150, 2)
    print(distance)

# Send data to ThingSpeak
def sendDataTs():
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%Z")
    #data = {"field1": distance}
    #ts.update(data)
    
        data = '[{{"timestamp":"{0}", "Distance":"{1:1f}"}}]'.format(now, distance)
        req = urllib2.Request(REST_API_URL, data)
        response = urllib2.urlopen(req)
        
        print ("[INFO] Data sent for 1 field: ", distance)
  
# Main function
def main(): 
    print ("[INFO] Initiating")
    while True:
        getDist()
        try:
            sendDataTs()
            time.sleep(1)
        except (KeyboardInterrupt):
            print ("[INFO] Finishing")
            break

''''--------------------------------------------------------------'''
if __name__ == '__main__':
    main()