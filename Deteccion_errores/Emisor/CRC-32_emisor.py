import socket
import random

def string_to_binary(s):
    return ''.join(format(ord(c), '08b') for c in s)

def crc32(binary_message):
    crc_table = []
    for i in range(256):
        crc = i
        for j in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xEDB88320
            else:
                crc >>= 1
        crc_table.append(crc)

    byte_message = int(binary_message, 2).to_bytes((len(binary_message) + 7) // 8, byteorder='big')

    crc = 0xFFFFFFFF
    for byte in byte_message:
        crc = crc_table[(crc ^ byte) & 0xFF] ^ (crc >> 8)

    crc ^= 0xFFFFFFFF
    crc_binary = format(crc, '032b')
    return crc_binary

def encode_crc32(message):
    binary_message = string_to_binary(message)
    crc_binary = crc32(binary_message)
    return binary_message + crc_binary

def apply_noise(binary_message, error_rate):
    noisy_message = []
    for bit in binary_message:
        if random.random() < error_rate:
            noisy_message.append('0' if bit == '1' else '1')
        else:
            noisy_message.append(bit)
    return ''.join(noisy_message)

def start_crc32_server(error_rate=0.0001):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 5002))
        s.listen()
        print("Emisor CRC-32 esperando conexiones...")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024).decode()
                encoded = encode_crc32(data)
                noisy_encoded = apply_noise(encoded, error_rate)
                conn.sendall(noisy_encoded.encode())

if __name__ == "__main__":
    start_crc32_server()
