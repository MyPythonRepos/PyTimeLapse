from picamera import PiCamera
import time
import paramiko
from scp import SCPClient

# SACAMOS LA FOTO
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
time.sleep(10)
camera.capture('./imgs/day.jpg')
camera.stop_preview()

