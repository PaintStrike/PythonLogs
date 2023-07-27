import time
import paramiko
import os
import sys

def leer_archivo_remoto(ruta_archivo_remoto, ultima_posicion_leida, ruta_archivo_local):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Conectar al servidor remoto
    ssh_client.connect('1.1.1.1', username='user', password='password')

    # Leer el contenido del archivo remoto desde la última posición leída
    with ssh_client.open_sftp() as sftp:
        with sftp.open(ruta_archivo_remoto, 'r') as archivo_remoto:
            archivo_remoto.seek(ultima_posicion_leida)
            contenido = archivo_remoto.read()

            # Guardar la nueva posición al final del archivo
            ultima_posicion_leida = archivo_remoto.tell()

    # Desconectar del servidor remoto
    ssh_client.close()

    return contenido, ultima_posicion_leida

if __name__ == "__main__":
    # Check if the local file path is provided as an argument
    if len(sys.argv) != 2:
        sys.exit(1)

    # Get the local file path from command-line arguments
    ruta_archivo_local = sys.argv[1]

    # Ruta del archivo de log remoto que quieres leer
    ruta_archivo_remoto = "/var/log/log.txt"

    # Inicializar la posición del archivo en 0
    ultima_posicion_leida = 0

    while True:
        try:
            # Leer el archivo remoto desde la última posición
            contenido_archivo, ultima_posicion_leida = leer_archivo_remoto(ruta_archivo_remoto, ultima_posicion_leida, ruta_archivo_local)

            # Guardar el contenido en tu servidor local si hay nuevos datos
            if contenido_archivo:
                with open(ruta_archivo_local, "ab") as archivo_local:
                    archivo_local.write(contenido_archivo)

               # print("Nuevos datos guardados con éxito.")
            else:
                print("No hay nuevos datos en el archivo remoto.")
                break
        except Exception as e:
            print("Error al leer o guardar el archivo:", e)
            break

        # Esperar 1,5 minutos antes de leer el archivo nuevamente
        time.sleep(90)
