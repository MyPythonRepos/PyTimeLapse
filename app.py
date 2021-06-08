from picamera import PiCamera
import time
import paramiko
from scp import SCPClient

# SACAMOS LA FOTO
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
time.sleep(10)
camera.capture('./imgs/image.jpg')
camera.stop_preview()

# ENVIAMOS LAS FOTOS AL SERVIDOR
server = '192.168.1.164'
port = 22
user = 'peter'
password = 'Tr0mp1c0n3s?'
def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

ssh = createSSHClient(server, port, user, password)
scp = SCPClient(ssh.get_transport())

scp.put('./imgs/image.jpg', './Pictures/')
