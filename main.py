from multiprocessing import connection
import cv2
from datetime import date
import socket
import uuid
import urllib.request
import ftplib
import time
import os

# REVISA SI HAY CONEXION A INTERNET

tiempo_fuera = 2 # tiempo en que la funcion se llama a si misma

host = host='http://google.com' # direccion de testeo

def connection_check():
    try:
        urllib.request.urlopen(host)
    except:
        time.sleep(tiempo_fuera)
        connection_check()

connection_check()

# ANTECEDENTES DE EQUIPO

fecha = date.today() 
nombre_equipo = socket.gethostname()
mac_equipo = '-'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)for ele in range(0,8*6,8)][::-1])
ip_externa = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
nombre_fichero = "SEGURIDAD_{}_{}_{}_{}.jpeg".format(str(fecha), str(nombre_equipo), str(mac_equipo), str(ip_externa))

# INICIO DE CAMARA
cam = cv2.VideoCapture(0)
ret, frame = cam.read()

# TOMAR CAPTURA
cv2.imwrite(nombre_fichero, frame)

# CERRAR CAMARA
cam.release()
cv2.destroyAllWindows()

# SUBIDA A SERVIDOR FTP
session = ftplib.FTP('tu_servidor_ftp','usuario','contraseña')
file = open(nombre_fichero,'rb')                  
session.storbinary('STOR '+nombre_fichero, file)    
file.close()                                   
session.quit()

# BORRAR FOTO
os.remove(nombre_fichero) 
