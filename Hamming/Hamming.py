import socket


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

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 5000))
        s.listen()
        print("Emisor esperando conexiones...")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024).decode()
                encoded = encode_message(data)
                conn.sendall(','.join(encoded).encode())

if __name__ == "__main__":
    start_server()