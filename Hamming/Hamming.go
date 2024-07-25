package main

import (
	"fmt"
	"strings"
)

// calculateParity calcula el bit de paridad para las posiciones dadas.
func calculateParity(bits []int, positions []int) int {
	parity := 0
	for _, pos := range positions {
		parity ^= bits[pos-1] // Operación XOR
	}
	return parity
}

// correctAndDecode corrige y decodifica un bloque de código Hamming (11,7).
func correctAndDecode(block string) ([]int, int) {
	// Posiciones de los bits de paridad
	parityPositions := map[int][]int{
		1: {1, 3, 5, 7, 9, 11},
		2: {2, 3, 6, 7, 10, 11},
		3: {4, 5, 6, 7},
		4: {8, 9, 10, 11},
	}

	// Convertir el bloque en una lista de enteros
	hammingCode := make([]int, 11)
	for i, bit := range block {
		hammingCode[i] = int(bit - '0')
	}

	// Detectar el error
	syndrome := 0
	for p, positions := range parityPositions {
		if calculateParity(hammingCode, positions) != 0 {
			syndrome += p
		}
	}

	// Corregir el bit si hay un error
	if syndrome != 0 {
		hammingCode[syndrome-1] ^= 1 // Corregir el bit
	}

	// Extraer los bits de datos: posiciones 3, 5, 6, 7, 9, 10, 11
	dataPositions := []int{3, 5, 6, 7, 9, 10, 11}
	dataBits := make([]int, len(dataPositions))
	for i, pos := range dataPositions {
		dataBits[i] = hammingCode[pos-1]
	}

	return dataBits, syndrome
}

// decodeMessage decodifica un mensaje codificado en Hamming (11,7) y devuelve el mensaje decodificado.
func decodeMessage(encodedMessage string) string {
	// Separar los bloques por comas
	blocks := strings.Split(encodedMessage, ",")

	decodedMessageBits := []int{}
	for _, block := range blocks {
		dataBits, syndrome := correctAndDecode(block)
		if syndrome != 0 {
			fmt.Printf("Error encontrado y corregido en el bloque: %s (Síndrome: %d)\n", block, syndrome)
		} else {
			fmt.Printf("Bloque sin errores detectados: %s\n", block)
		}
		decodedMessageBits = append(decodedMessageBits, dataBits...)
	}

	// Convertir los bits a caracteres ASCII de 7 bits
	var asciiChars []rune
	for i := 0; i < len(decodedMessageBits); i += 7 {
		if i+7 > len(decodedMessageBits) {
			break
		}
		charBits := decodedMessageBits[i : i+7]
		charValue := 0
		for j, bit := range charBits {
			charValue += bit << (6 - j)
		}
		asciiChars = append(asciiChars, rune(charValue))
	}

	return string(asciiChars)
}

func main() {
	// Solicitar la cadena de caracteres codificados en Hamming (11,7) separados por comas
	var input string
	fmt.Println("Introduce la cadena de caracteres codificados en Hamming (11,7) separados por comas:")
	fmt.Scanln(&input)

	// Decodificar el mensaje
	decodedMessage := decodeMessage(input)
	fmt.Printf("Mensaje decodificado: %s\n", decodedMessage)
}
