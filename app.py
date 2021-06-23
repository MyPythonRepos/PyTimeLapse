from picamera import PiCamera
import time
import paramiko
from scp import SCPClient
from datetime import datetime
from configparser import ConfigParser

# Leer fichero de configuracion
config_object = ConfigParser()
config_object.read("config.ini")
hostinfo = config_object["HOSTCONFIG"]
src_folder = hostinfo["source_folder"]

print("Inicializamos el timelapse")

# SACAMOS LA FOTO
camera = PiCamera()
while True:
  ahora = datetime.now()
  date_time = ahora.strftime("%y%m%d_%H%M%S")
  print(date_time)
  camera.resolution = (1024, 768)
  camera.start_preview()
  time.sleep(10)
  camera.capture(src_folder + date_time + '.jpg')
  camera.stop_preview()
  print("Fotografía tomada")

print("Finaliza el timelapse")

