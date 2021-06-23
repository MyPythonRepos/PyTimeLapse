# PyTimeLapse


Imagen base: Linux raspberrypi 5.10.17-v7+ #1414 SMP Fri Apr 30 13:18:35 BST 2021 armv7l

Python:
  - Python 3.7.3
  - pip 18.1 from /usr/lib/python3/dist-packages/pip (python 3.7)

## Planteamiento inicial:

  Creamos dos scripts python. El primero (app.py) será el encargado
  de tomar las fotografías. El segundo (transfer_files.py) se encargará de
  mover las imágenes obtenidas desde la raspberry al servidor.

  Para ejecutar ambos scripts utilizaremos dos tareas cron: la primera
  ejecutará app.py cada vez que la raspberry se inicie; el segundo se irá
  ejecutando de forma periódica para evitar que el almacenamiento
  de la raspberry se llene.

## Requerimientos:

  Una vez clonado el repositorio, es necesario crear en la carpeta raíz los
  siguientes archivos:

  * secrets.py, con los siguientes valores
    * user = "usuario_servidor"
    * password = "password_servidor"

  * config.ini, con la siguiente estructura:
    [SERVERCONFIG]
    host = "nombre_del_servidor"
    server_ip = ip_del_servidor
    port = puerto_ssh
    destination_folder = destino_de_las_imagenes

    [HOSTCONFIG]
    source_folder = ./imgs [ubicación por defecto de las imágenes tomadas]

## Links:

   - https://picamera.readthedocs.io/en/release-1.13/recipes1.html#
   - https://paramiko-docs.readthedocs.io/en/1.15/index.html
