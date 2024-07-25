import binascii

def string_to_binary(s):
    return ''.join(format(ord(c), '08b') for c in s)

def crc32(binary_message):
    # Convert binary string to bytes
    byte_message = int(binary_message, 2).to_bytes((len(binary_message) + 7) // 8, byteorder='big')
    # Calculate CRC-32 using the binascii library
    crc = binascii.crc32(byte_message) & 0xffffffff
    # Convert CRC-32 result to binary string
    crc_binary = format(crc, '032b')
    return crc_binary

def main():
    # Step 1: Convert word to binary
    word = input("Enter a word to convert to binary: ")
    binary_word = string_to_binary(word)
    print(f"Binary representation of '{word}': {binary_word}")
    
    # Step 2: Request binary message
    binary_message = input("Enter a binary message: ")
    
    # Step 3: Compute CRC-32
    crc_binary = crc32(binary_message)
    print(f"CRC-32 of the binary message: {crc_binary}")
    
    # Step 4: Concatenate CRC to the binary message
    result_message = binary_message + crc_binary
    print(f"Binary message with CRC-32: {result_message}")

if __name__ == "__main__":
    main()
