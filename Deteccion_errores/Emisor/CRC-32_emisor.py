def string_to_binary(s):
    return ''.join(format(ord(c), '08b') for c in s)

def crc32(binary_message):
    # Inicializar la tabla CRC-32
    crc_table = []
    for i in range(256):
        crc = i
        for j in range(8):
            if (crc & 1):
                crc = (crc >> 1) ^ 0xEDB88320
            else:
                crc >>= 1
        crc_table.append(crc)

    # Convertir el mensaje binario a bytes
    byte_message = int(binary_message, 2).to_bytes((len(binary_message) + 7) // 8, byteorder='big')

    # Calcular el CRC-32
    crc = 0xFFFFFFFF
    for byte in byte_message:
        crc = crc_table[(crc ^ byte) & 0xFF] ^ (crc >> 8)

    crc ^= 0xFFFFFFFF

    crc_binary = format(crc, '032b')
    return crc_binary

def main():
    word = input("Enter a word to convert to binary: ")
    binary_word = string_to_binary(word)
    print(f"Binary representation of '{word}': {binary_word}")
    
    crc_binary = crc32(binary_word)
    print(f"CRC-32 of the binary message: {crc_binary}")
    
    result_message = binary_word + crc_binary
    print(f"Binary message with CRC-32: {result_message}")

if __name__ == "__main__":
    main()
