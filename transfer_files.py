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
  return (server_host, server_ip, server_port, dst_folder, src_folder)


# Establece conexión con el servidor para la transferencia de archivos
def createSSHClient(server_ip, server_port):
  client = paramiko.SSHClient()
  client.load_system_host_keys()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  try:
    client.connect(server_ip, server_port, secrets.user, secrets.password, timeout=10)
    print("Conexión realizada")
    return client
  except (NoValidConnectionsError, BadHostKeyException, AuthenticationException, SSHException, socket.error) as e:
    print("Hay un error")
    print(e)
    exit(1)


# Si hay imagenes en el directorio origen se inicia el proceso de transferencia
def transferir_archivos(server_host, server_ip, server_port, dst_folder, src_folder):
  folder = os.listdir(src_folder)
  if len(folder) == 0:
    print("El directorio está vacío")
  else:
    print("Conectamos con el cliente")
    ssh = createSSHClient(server_ip, server_port)
    scp = SCPClient(ssh.get_transport())
    print("Empieza la transferencia de archivos")
    scp.put(src_folder, recursive=True, remote_path=dst_folder)
    # Se vacía el directorio de las imagenes
    for file in os.listdir(src_folder):
      os.remove(src_folder + '/' + file)

def main():
  print("Empieza script")
  server_host, server_ip, server_port, dst_folder, src_folder = leer_configuracion()
  transferir_archivos(server_host, server_ip, server_port, dst_folder, src_folder)
  print("Finaliza el script")


if __name__ == '__main__':
  main()
