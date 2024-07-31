import socket
import subprocess

def send_receive(message, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', port))
        s.sendall(message.encode())
        return s.recv(1024).decode()

def main():

    print('-------------------Bienvenido al programa de codificación de mensajes-------------------\n')
    
    salir = False
    while not salir:
        print('Por favor ingrese el metodo de codificación de su mensaje')
        print('1. Hamming (corrector de errores)')
        print('2. CRC-32 (detector de errores)')
        print('3. Salir\n')
        op = input ('Ingrese el número de la opción deseada: ')
        if op == '1':
            print('-------------------Codificación Hamming-------------------\n\n')
            # Esperar a que los servidores estén listos
            input("Presiona Enter cuando los servidores estén listos...")
            # Obtener el mensaje del usuario
            message = input("Introduce un mensaje para codificar: ")
            # Enviar al emisor y recibir la codificación
            encoded = send_receive(message, 5000)
            print("Mensaje codificado:", encoded)
            # Enviar al receptor y recibir la decodificación
            decoded = send_receive(encoded, 5001)
            print("Mensaje decodificado:", decoded)
        elif op == '2':
            #pending...
            pass
        elif op == '3':
            salir = True
        else:
            print('Opción no válida')
    # Iniciar el emisor y receptor

    

if __name__ == "__main__":
    main()