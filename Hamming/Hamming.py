import socket
import random
import sys


def encode_hamming_11_7(data):
    # Asegurarse de que la entrada sea de 7 bits
    assert len(data) == 7, "La entrada debe ser de 7 bits"
    
    # Crear el código Hamming de 11 bits
    code = [0] * 11
    
    # Colocar los bits de datos en las posiciones correctas
    code[2] = data[0]
    code[4] = data[1]
    code[5] = data[2]
    code[6] = data[3]
    code[8] = data[4]
    code[9] = data[5]
    code[10] = data[6]
    
    # Calcular los bits de paridad
    code[0] = code[2] ^ code[4] ^ code[6] ^ code[8] ^ code[10]  # Paridad 1
    code[1] = code[2] ^ code[5] ^ code[6] ^ code[9] ^ code[10]  # Paridad 2
    code[3] = code[4] ^ code[5] ^ code[6]  # Paridad 4
    code[7] = code[8] ^ code[9] ^ code[10]  # Paridad 8
    
    return code

def encode_message(message):
    encoded = []
    for char in message:
        # Convertir el carácter a su representación binaria de 7 bits
        binary = format(ord(char), '07b')
        # Convertir la cadena binaria a una lista de enteros
        data = [int(bit) for bit in binary]
        # Codificar los 7 bits en Hamming (11,7)
        hamming = encode_hamming_11_7(data)
        # Convertir la lista de bits a una cadena y añadirla al resultado
        encoded.append(''.join(map(str, hamming)))
    return encoded

def add_noise(encoded_message, error_rate):
    noisy_message = []
    for block in encoded_message:
        noisy_block = list(block)
        for i in range(len(noisy_block)):
            if random.random() < error_rate:
                noisy_block[i] = '1' if noisy_block[i] == '0' else '0'
        noisy_message.append(''.join(noisy_block))
    return noisy_message

def start_server(port, error_rate):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen()
        print(f"Emisor esperando conexiones en el puerto {port} (Tasa de error: {error_rate})...")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024).decode()
                encoded = encode_message(data)
                noisy_encoded = add_noise(encoded, error_rate)
                
                # Imprimir mensaje original y con ruido para comparación
                print("Mensaje codificado original:", ','.join(encoded))
                print("Mensaje codificado con ruido:", ','.join(noisy_encoded))
                
                conn.sendall(','.join(noisy_encoded).encode())

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    error_rate = float(sys.argv[2]) if len(sys.argv) > 1 else 0.001
    start_server(port, error_rate)