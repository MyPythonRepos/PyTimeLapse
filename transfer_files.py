import secrets
import os
from sys import exit
import socket
import paramiko
from paramiko.ssh_exception import NoValidConnectionsError, BadHostKeyException, AuthenticationException, SSHException
from scp import SCPClient

print("Empieza script")

'''
Establecemos la conexión con el servidor para
trasferir los archivos.
'''
server = '192.168.1.164'
port = 22
user = secrets.user
password = secrets.password
def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(server, port, user, password, timeout=10)
        print("Conexión realizada")
        return client
    except (NoValidConnectionsError, BadHostKeyException, AuthenticationException, SSHException, socket.error) as e:
        print("Hay un error")
        print(e)
        exit(1)


'''
Iniciamos el proceso de transferencia, comprobando si el directorio imgs
contiene algún archivo a transferir. 
'''
folder = os.listdir('./imgs')
if len(folder) == 0:
    print("Directory is empty")
else:
    print("Conectamos con el cliente")
    ssh = createSSHClient(server, port, user, password)
    scp = SCPClient(ssh.get_transport())
    print("Empieza el traspaso")
    folder = os.scandir('./imgs')
    for file in folder:
        print(file.name)
        scp.put(file, './Pictures/')

print("Finaliza el script")
