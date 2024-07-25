import binascii

def string_to_binary(s):
    return ''.join(format(ord(c), '08b') for c in s)



def main():
    # Step 1: Convert word to binary
    word = input("Enter a word to convert to binary: ")
    binary_word = string_to_binary(word)
    print(f"Binary representation of '{word}': {binary_word}")
    


if __name__ == "__main__":
    main()
