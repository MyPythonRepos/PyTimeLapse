import logging
import os
import paramiko
import secrets
import socket
from configparser import ConfigParser
from paramiko.ssh_exception import NoValidConnectionsError, BadHostKeyException, AuthenticationException, SSHException
from scp import SCPClient
from sys import exit


# Leer fichero de configuracion
def leer_configuracion():
  config_object = ConfigParser()
  config_object.read("config.ini")
  serverinfo = config_object["SERVERCONFIG"]
  server_host = serverinfo["host"]
  server_ip = serverinfo["server_ip"]
  server_port = serverinfo["port"]
  dst_folder = serverinfo["destination_folder"]
  hostinfo = config_object["HOSTCONFIG"]
  src_folder = hostinfo["source_folder"]
  if not os.path.isdir(src_folder):
    os.makedirs(src_folder)
  log_folder = hostinfo["log_folder"]
  if not os.path.isdir(log_folder):
    os.makedirs(log_folder)
  return (server_host, server_ip, server_port, dst_folder, src_folder, log_folder)


# Establece conexión con el servidor para la transferencia de archivos
def createSSHClient(server_ip, server_port):
  client = paramiko.SSHClient()
  client.load_system_host_keys()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  try:
    client.connect(server_ip, server_port, secrets.user, secrets.password, timeout=10)
    logging.info("Conexión realizada con el servidor.")
    return client
  except (NoValidConnectionsError, BadHostKeyException, AuthenticationException, SSHException, socket.error) as e:
    logging.error("No se ha podido conectar con el servidor.")
    logging.error(e)
    exit(1)


# Si hay imagenes en el directorio origen se inicia el proceso de transferencia
def transferir_archivos(server_host, server_ip, server_port, dst_folder, src_folder):
  folder = os.listdir(src_folder)
  if len(folder) == 0:
    logging.warning("El directorio de imágenes está vacío")
  else:
    ssh = createSSHClient(server_ip, server_port)
    scp = SCPClient(ssh.get_transport())
    logging.info("Empieza la transferencia de imágenes.")
    scp.put(src_folder, recursive=True, remote_path=dst_folder)
    logging.info("Transferidos " + str(len(os.listdir(src_folder))) + " archivos.")
    # Se vacía el directorio de las imagenes
    imagenes = []
    for file in os.listdir(src_folder):
      imagenes.append(file)
      os.remove(src_folder + '/' + file)
    lista_imagenes = ";".join(map(str,imagenes))
    logging.info("Eliminados los archivos: " + lista_imagenes)
    logging.info("Directorio de imágenes vaciado correctamente.")

def main():
  server_host, server_ip, server_port, dst_folder, src_folder, log_folder = leer_configuracion()
  logging.basicConfig(filename=log_folder + 'transfer.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%H:%S%p' )
  logging.info("Iniciado script de transferencia de archivos.")
  transferir_archivos(server_host, server_ip, server_port, dst_folder, src_folder)
  logging.info("Finalizado el script de transferencia.")


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    logging.error("Script interrumpido por teclado")
