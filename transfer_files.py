import os
from sys import exit
import socket
import paramiko
from paramiko.ssh_exception import NoValidConnectionsError, BadHostKeyException, AuthenticationException, SSHException
from scp import SCPClient

# ENVIAMOS LAS FOTOS AL SERVIDOR
server = '192.168.1.164'
port = 22
user = 'peter'
password = 'Tr0mp1c0n3s?'
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
        exit


ssh = createSSHClient(server, port, user, password)
print("empieza traspaso")
scp = SCPClient(ssh.get_transport())

folder = os.scandir('./imgs')
for file in folder:
    scp.put(file, './Pictures/')
