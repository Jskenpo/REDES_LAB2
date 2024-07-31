import socket
import subprocess

def send_receive(message, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', port))
        s.sendall(message.encode())
        return s.recv(1024).decode()

def main():
    # Iniciar el emisor y receptor
    subprocess.Popen(["python", "Hamming/Hamming.py"])
    subprocess.Popen(["go", "run", "Hamming/Hamming.go"])

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

if __name__ == "__main__":
    main()