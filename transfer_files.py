import secrets
import os
import socket
import paramiko
from sys import exit
from paramiko.ssh_exception import NoValidConnectionsError, BadHostKeyException, AuthenticationException, SSHException
from scp import SCPClient
from configparser import ConfigParser

print("Empieza script")

# Leer fichero de configuracion
config_object = ConfigParser()
config_object.read("config.ini")
serverinfo = config_object["SERVERCONFIG"]
server_host = serverinfo["host"]
server_ip = serverinfo["server_ip"]
server_port = serverinfo["port"]
dst_folder = serverinfo["destination_folder"]
hostinfo = config_object["HOSTCONFIG"]
src_folder = hostinfo["source_folder"]

# Establecemos la conexión con el servidor para la transferencia de archivos
def createSSHClient():
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
folder = os.listdir(src_folder)
if len(folder) == 0:
    print("El directorio está vacío")
else:
    print("Conectamos con el cliente")
    ssh = createSSHClient()
    scp = SCPClient(ssh.get_transport())
    print("Empieza la transferencia de archivos")
    folder = os.scandir(src_folder)
    for file in folder:
        print(file.name)
        scp.put(file, dst_folder)
        os.remove(file) 

print("Finaliza el script")
