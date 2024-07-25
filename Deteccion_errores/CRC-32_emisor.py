

Mensaje_estudiante = ""

def CRC_32(mensaje):
    # Se inicializa el CRC con 0xFFFFFFFF
    CRC = 0xFFFFFFFF
    # Se realiza la operacion XOR entre el CRC y el mensaje
    for i in mensaje:
        CRC = CRC ^ i
        # Se realizan 8 operaciones de XOR
        for j in range(8):
            # Se realiza la operacion AND entre el CRC y 1
            if CRC & 1:
                # Se realiza la operacion XOR entre el CRC y 0xEDB88320
                CRC = (CRC >> 1) ^ 0xEDB88320
            else:
                CRC = CRC >> 1
    return CRC

def main():
    global Mensaje_estudiante
    # Se solicita al usuario el mensaje
    Mensaje_estudiante = input("Ingrese el mensaje: ")
    # Se convierte el mensaje a bytes
    mensaje = Mensaje_estudiante.encode()
    # Se calcula el CRC
    CRC = CRC_32(mensaje)
    # Se imprime el CRC
    print(f"CRC-32: {CRC}")


if __name__ == "__main__":
    main()