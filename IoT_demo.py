#!/usr/bin/python
## python3
import RPi.GPIO as GPIO
import time
from datetime import datetime
import requests

#GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

PIN_TRIGGER = 7
PIN_ECHO = 11

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

GPIO.output(PIN_TRIGGER, GPIO.LOW)

REST_API_URL = "https://api.powerbi.com/beta/efdf19a6-7ca0-43bd-b3aa-f960679015b0/datasets/19621eee-34ad-44f3-bf8d-5314b0f758a1/rows?key=28eMKQOiiqZ9IKVCjUnmfHMkyOYjOpnwEdlyHQeEOMT9lqSIaCd3LT174QU3GJCPwdEj6Q%2FvtERUCQTBe%2FOdtQ%3D%3D"

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
    

# Send data to ThingSpeak
def sendDataTs():
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%Z")
    #data = {"field1": distance}
    #ts.update(data)
    
        data = '[{{"timestamp":"{0}", "Distance":"{1:1f}"}}]'.format(now, distance)
        r = requests.post(REST_API_URL, data=data)
        
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