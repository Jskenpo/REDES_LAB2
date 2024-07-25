package main

import (
	"bufio"
	"encoding/binary"
	"fmt"
	"hash/crc32"
	"os"
	"strconv"
)

func binaryToString(binStr string) (string, error) {
	if len(binStr)%8 != 0 {
		return "", fmt.Errorf("invalid binary string length")
	}
	bytes := make([]byte, len(binStr)/8)
	for i := 0; i < len(binStr); i += 8 {
		byteVal, err := strconv.ParseUint(binStr[i:i+8], 2, 8)
		if err != nil {
			return "", err
		}
		bytes[i/8] = byte(byteVal)
	}
	return string(bytes), nil
}

func crc32Check(binaryMessage string) (string, bool) {
	if len(binaryMessage) <= 32 {
		return "", false
	}

	messagePart := binaryMessage[:len(binaryMessage)-32]
	crcPart := binaryMessage[len(binaryMessage)-32:]

	messageBytes := make([]byte, len(messagePart)/8)
	for i := 0; i < len(messagePart); i += 8 {
		byteVal, err := strconv.ParseUint(messagePart[i:i+8], 2, 8)
		if err != nil {
			return "", false
		}
		messageBytes[i/8] = byte(byteVal)
	}

	crc := crc32.ChecksumIEEE(messageBytes)
	crcBinary := fmt.Sprintf("%032b", crc)

	return messagePart, crcBinary == crcPart
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Enter a binary message with CRC-32: ")
	binaryMessage, _ := reader.ReadString('\n')
	binaryMessage = binaryMessage[:len(binaryMessage)-1] // Remove newline character

	messagePart, valid := crc32Check(binaryMessage)
	if valid {
		message, err := binaryToString(messagePart)
		if err != nil {
			fmt.Println("Error converting binary to string:", err)
			return
		}
		fmt.Println("No errors detected. Original message:", message)
	} else {
		fmt.Println("Errors detected. Message discarded.")
	}
}
