import logging
import os
import paramiko
import sys
import time
from configparser import ConfigParser
from datetime import datetime
from picamera import PiCamera
from scp import SCPClient


def fecha_y_hora():
  ahora = datetime.now()
  return ahora.strftime("%y%m%d_%H%M%S")


#print(os.path.basename(__file__))


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
    logging.info("Fotografía tomada: " + photo_name)


def main():
  logging.basicConfig(filename='/var/log/photo.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%H:%S%p' )
  logging.info("Inicializamos el timelapse")
  src_folder, log_folder = leer_configuracion()
  tomar_fotografias(src_folder)
  logging.info("Finaliza el timelapse")


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    logging.error("KeyboardInterrupt - Timelapse interrumpido por teclado.")
    sys.exit()

