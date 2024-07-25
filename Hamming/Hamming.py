def calculate_parity(bits, positions):
    parity = 0
    for pos in positions:
        parity ^= bits[pos-1]  # Operación XOR
    return parity

def encode_hamming_11_7(data_bits):
    # Posiciones de los bits de paridad
    parity_positions = {
        1: [1, 3, 5, 7, 9, 11],
        2: [2, 3, 6, 7, 10, 11],
        3: [4, 5, 6, 7],
        4: [8, 9, 10, 11]
    }

    # Insertar los bits de datos en las posiciones correspondientes
    hamming_code = [0] * 11
    data_positions = [3, 5, 6, 7, 9, 10, 11]
    for i, bit in zip(data_positions, data_bits):
        hamming_code[i-1] = bit

    # Calcular los bits de paridad
    for p in parity_positions:
        hamming_code[p-1] = calculate_parity(hamming_code, parity_positions[p])

    return hamming_code

def encode_message(message):
    hamming_codes = []
    for char in message:
        # Obtener el valor ASCII del carácter y luego su representación binaria de 7 bits
        ascii_value = ord(char)
        binary_representation = f"{ascii_value:07b}"  # 7 bits
        data_bits = [int(bit) for bit in binary_representation]

        # Codificar en Hamming (11,7)
        hamming_code = encode_hamming_11_7(data_bits)
        hamming_codes.append(''.join(map(str, hamming_code)))

    return hamming_codes

# Solicitar un mensaje al usuario
message = input("Introduce un mensaje para codificar: ")
encoded_message = encode_message(message)

# Mostrar los resultados
print("Códigos Hamming (11,7) separados por comas:")
print(",".join(encoded_message))
