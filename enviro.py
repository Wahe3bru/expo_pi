#!/usr/bin/env python

import sys
import time
import requests
from datetime import datetime
from picamera import PiCamera, Color
from envirophat import light, weather, motion, analog

unit = 'hPa' # Pressure unit, can be either hPa (hectopascals) or Pa (pascals)
REST_API_URL = "https://api.powerbi.com/beta/efdf19a6-7ca0-43bd-b3aa-f960679015b0/datasets/19621eee-34ad-44f3-bf8d-5314b0f758a1/rows?key=28eMKQOiiqZ9IKVCjUnmfHMkyOYjOpnwEdlyHQeEOMT9lqSIaCd3LT174QU3GJCPwdEj6Q%2FvtERUCQTBe%2FOdtQ%3D%3D"

camera = PiCamera()

# camera settings
camera.rotation = 180
camera.resolution = (640, 480)
camera.annotate_text = "Wanted for flying under the influence"
camera.annotate_text_size = 55
camera.annotate_background = Color('white')
camera.annotate_background = Color('red')
camera.image_effect = 'posterise'

def make_wanted():
    camera.start_preview(alpha=200)
    time.sleep(2)
    camera.capture('/home/pi/Desktop/test_pix/{}.jpg'.format(now))
    camera.stop_preview()

def write(line):
    sys.stdout.write(line)
    sys.stdout.flush()

write("--- Enviro pHAT Monitoring ---")

prev_acc_vals = [1500, 800, 200]
try:
    while True:
        #get values
        rgb = light.rgb()
        mag_values = motion.magnetometer()
        acc_values = [round(x,2) for x in motion.accelerometer()]
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%Z")
        
        # prepare data to be sent
        data = ''' [{{
"Timestamp": "{ts}",
"Temp": "{t:.1}",
"Pressure": "{p:.1f}",
"Altitude": "{a:.1f}",
"Light": "{c:.1f}",
"Heading": "{h:.1f}",
"Magnetometer_x": "{mx}",
"Magnetometer_y": "{my}",
"Magnetometer_z": "{mz}",
"Accelerometer_x": "{ax:.1f}",
"Accelerometer_y": "{ay:.1f}",
"Accelerometer_z": "{az:.1f}"

}}] '''.format(
        ts = now,
        a = weather.altitude(), # Supply your local qnh for more accurate readings
        t = weather.temperature(),
        p = weather.pressure(unit=unit),
        c = light.light(),
        h = motion.heading(),
        mx = mag_values[0],
        my = mag_values[1],
        mz = mag_values[2],
        ax = acc_values[0],
        ay = acc_values[1],
        az = acc_values[2]
    )
        # uncomment to stream sensor data
        # r = requests.post(REST_API_URL, data=data)
        # original output to display: stdout
        output = """
Timestamp: {ts}
Temp: {t:.2}c
Pressure: {p:.2f}{unit}
Altitude: {a:.2f}m
Light: {c}
Heading: {h}
Magnetometer: {mx} {my} {mz}
Accelerometer: {ax}g {ay}g {az}g

""".format(
        ts = now,
        unit = unit,
        a = weather.altitude(), # Supply your local qnh for more accurate readings
        t = weather.temperature(),
        p = weather.pressure(unit=unit),
        c = light.light(),
        h = motion.heading(),
        mx = mag_values[0],
        my = mag_values[1],
        mz = mag_values[2],
        ax = acc_values[0],
        ay = acc_values[1],
        az = acc_values[2]
    )
        output = output.replace("\n","\n\033[K")
        write(output)
        lines = len(output.split("\n"))
        write("\033[{}A".format(lines - 1))

        
        if mag_values[0] - prev_acc_vals[0] > 1000:
            make_wanted()
            prev_acc_vals = mag_values
        elif mag_values[1] - prev_acc_vals[1] > 1000:
            make_wanted()
            prev_acc_vals = mag_values
        elif mag_values[2] - prev_acc_vals[2] > 500:
            make_wanted()
            prev_acc_vals = mag_values
        else:
            prev_acc_vals = mag_values
        time.sleep(1)
except KeyboardInterrupt:
    pass
