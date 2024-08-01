import socket

def send_receive(message, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', port))
        s.sendall(message.encode())
        return s.recv(1024).decode()

def send_receive_CRC(message, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', port))
        s.sendall((message + "\n").encode())
        s.shutdown(socket.SHUT_WR)  # Cerramos la parte de escritura del socket para indicar que hemos terminado de enviar
        response = []
        while True:
            data = s.recv(1024)
            if not data:
                break
            response.append(data.decode())
        return ''.join(response)

def main():
    print('-------------------Bienvenido al programa de codificación de mensajes-------------------\n')
    
    salir = False
    while not salir:
        print('Por favor ingrese el metodo de codificación de su mensaje')
        print('1. Hamming (corrector de errores)')
        print('2. CRC-32 (detector de errores)')
        print('3. Salir\n')
        op = input('Ingrese el número de la opción deseada: ')
        if op == '1':
            print('-------------------Codificación Hamming-------------------\n\n')
            input("Presiona Enter cuando los servidores estén listos...")
            message = input("Introduce un mensaje para codificar: ")
            encoded = send_receive(message, 5000)
            print("Mensaje codificado:", encoded)
            decoded = send_receive(encoded, 5001)
            print("Mensaje decodificado:", decoded)
        elif op == '2':
            print('-------------------Codificación CRC-32-------------------\n\n')
            input("Presiona Enter cuando los servidores estén listos...")
            message = input("Introduce un mensaje para codificar: ")
            encoded = send_receive_CRC(message, 5002)
            print("Mensaje codificado:", encoded)
            decoded = send_receive_CRC(encoded, 5003)
            print("Resultado del receptor:", decoded)
        elif op == '3':
            salir = True
        else:
            print('Opción no válida')
    

if __name__ == "__main__":
    main()
