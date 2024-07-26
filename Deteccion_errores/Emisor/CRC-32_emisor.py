import binascii

def string_to_binary(s):
    return ''.join(format(ord(c), '08b') for c in s)

def crc32(binary_message):

    byte_message = int(binary_message, 2).to_bytes((len(binary_message) + 7) // 8, byteorder='big')

    crc = binascii.crc32(byte_message) & 0xffffffff

    crc_binary = format(crc, '032b')
    return crc_binary

def main():

    word = input("Enter a word to convert to binary: ")
    binary_word = string_to_binary(word)
    print(f"Binary representation of '{word}': {binary_word}")
    
    binary_message = input("Enter a binary message: ")
    
    crc_binary = crc32(binary_message)
    print(f"CRC-32 of the binary message: {crc_binary}")
    
    result_message = binary_message + crc_binary
    print(f"Binary message with CRC-32: {result_message}")

if __name__ == "__main__":
    main()
