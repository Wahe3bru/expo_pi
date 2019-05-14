#pi_cam
from picamera import PiCamera, Color
from time import sleep

camera = PiCamera()

#settings
camera.rotation = 180
camera.annotate_text = "Wanted for flying under the influence"
camera.annotate_text_size = 150
camera.annotate_background = Color('white')
camera.annotate_background = Color('red')
camera.image_effect = 'posterise'

camera.start_preview(alpha=200)
sleep(5)
camera.capture('/home/pi/Desktop/test1.jpg')
camera.stop_preview()