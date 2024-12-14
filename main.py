import cv2
from datetime import date
import socket
import uuid
import urllib.request
import ftplib
import time
import os


# CONFIGURACIÓN DE CONEXIÓN
TIEMPO_ESPERA = 2  # tiempo en que la función se llama a sí misma si no hay conexión
HOST = 'http://google.com'  # dirección de testeo

# CONFIGURACIÓN FTP
FTP_SERVIDOR = 'tu_servidor_ftp'
FTP_USUARIO = 'usuario'
FTP_CONTRASEÑA = 'contraseña'


def connection_check():
    """Verifica la conexión a internet."""
    while True:
        try:
            urllib.request.urlopen(HOST)
            print("Conexión a Internet establecida.")
            break
        except urllib.error.URLError:
            print("No hay conexión a Internet. Reintentando...")
            time.sleep(TIEMPO_ESPERA)


def obtener_antecedentes_equipo():
    """Obtiene los antecedentes del equipo (fecha, nombre, MAC, IP externa)."""
    fecha = date.today()
    nombre_equipo = socket.gethostname()
    mac_equipo = '-'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8*6, 8)][::-1])
    ip_externa = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
    nombre_fichero = f"SEGURIDAD_{fecha}_{nombre_equipo}_{mac_equipo}_{ip_externa}.jpeg"
    return nombre_fichero


def tomar_captura():
    """Toma una foto usando la cámara."""
    with cv2.VideoCapture(0) as cam:
        ret, frame = cam.read()
        if ret:
            return frame
        else:
            raise Exception("No se pudo capturar la imagen de la cámara.")


def subir_a_ftp(nombre_fichero):
    """Sube la imagen al servidor FTP."""
    try:
        with ftplib.FTP(FTP_SERVIDOR, FTP_USUARIO, FTP_CONTRASEÑA) as session:
            with open(nombre_fichero, 'rb') as file:
                session.storbinary(f'STOR {nombre_fichero}', file)
            print("Archivo subido con éxito.")
    except ftplib.all_errors as e:
        print(f"Error al subir archivo al FTP: {e}")


def borrar_foto(nombre_fichero):
    """Elimina la foto capturada."""
    try:
        os.remove(nombre_fichero)
        print(f"Archivo {nombre_fichero} eliminado.")
    except OSError as e:
        print(f"Error al eliminar el archivo {nombre_fichero}: {e}")


def main():
    # Verificar conexión a Internet
    connection_check()

    # Obtener los antecedentes del equipo
    nombre_fichero = obtener_antecedentes_equipo()

    # Tomar una captura de la cámara
    try:
        frame = tomar_captura()
        cv2.imwrite(nombre_fichero, frame)
        print(f"Imagen guardada como {nombre_fichero}.")
    except Exception as e:
        print(f"Error al capturar la imagen: {e}")
        return

    # Subir la imagen al servidor FTP
    subir_a_ftp(nombre_fichero)

    # Eliminar la imagen después de subirla
    borrar_foto(nombre_fichero)


if __name__ == '__main__':
    main()
