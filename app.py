import os
import paramiko
import time
from configparser import ConfigParser
from datetime import datetime
from picamera import PiCamera
from scp import SCPClient


def fecha_y_hora():
  ahora = datetime.now()
  return ahora.strftime("%y%m%d_%H%M%S")


print(os.path.basename(__file__))


# LEER FICHERO DE CONFIGURACION
def leer_configuracion():
  config_object = ConfigParser()
  config_object.read("config.ini")
  hostinfo = config_object["HOSTCONFIG"]
  src_folder = hostinfo["source_folder"]
  if not os.path.isdir(src_folder):
    os.makedirs(src_folder)
  log_folder = hostinfo["log_folder"]
  if not os.path.isdir(log_folder):
    os.makedirs(log_folder)
  return (src_folder, log_folder)


# PROCESO DE TOMA DE FOTOGRAFIAS
def tomar_fotografias(src_folder):
  camera = PiCamera()
  while True:
    camera.resolution = (1024, 768)
    camera.start_preview()
    time.sleep(10)
    photo_name = fecha_y_hora() + '.jpg'
    camera.capture(src_folder + '/' + photo_name)
    camera.stop_preview()
    print("Fotografía tomada: " + photo_name)

if __name__ == '__main__':
  print("Inicializamos el timelapse")
  src_folder, log_folder = leer_configuracion()
  tomar_fotografias(src_folder)
  print("Finaliza el timelapse")

