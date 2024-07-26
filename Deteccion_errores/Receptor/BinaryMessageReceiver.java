package Receptor;
import java.util.Scanner;
import java.util.zip.CRC32;

public class BinaryMessageReceiver {
    
    public static String binaryToString(String binStr) throws IllegalArgumentException {
        if (binStr.length() % 8 != 0) {
            throw new IllegalArgumentException("Invalid binary string length");
        }
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < binStr.length(); i += 8) {
            String byteString = binStr.substring(i, i + 8);
            int byteValue = Integer.parseInt(byteString, 2);
            result.append((char) byteValue);
        }
        return result.toString();
    }

    public static boolean crc32Check(String binaryMessage) {
        if (binaryMessage.length() <= 32) {
            return false;
        }
        
        String messagePart = binaryMessage.substring(0, binaryMessage.length() - 32);
        String crcPart = binaryMessage.substring(binaryMessage.length() - 32);
        
        byte[] messageBytes = new byte[messagePart.length() / 8];
        for (int i = 0; i < messagePart.length(); i += 8) {
            String byteString = messagePart.substring(i, i + 8);
            int byteValue = Integer.parseInt(byteString, 2);
            messageBytes[i / 8] = (byte) byteValue;
        }

        CRC32 crc32 = new CRC32();
        crc32.update(messageBytes);
        long crcValue = crc32.getValue();
        String crcBinary = String.format("%32s", Long.toBinaryString(crcValue)).replace(' ', '0');
        
        return crcBinary.equals(crcPart);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a binary message with CRC-32: ");
        String binaryMessage = scanner.nextLine();
        
        boolean valid = crc32Check(binaryMessage);
        if (valid) {
            String messagePart = binaryMessage.substring(0, binaryMessage.length() - 32);
            try {
                String message = binaryToString(messagePart);
                System.out.println("No errors detected. Original message: " + message);
            } catch (IllegalArgumentException e) {
                System.out.println("Error converting binary to string: " + e.getMessage());
            }
        } else {
            System.out.println("Errors detected. Message discarded.");
        }
        
        scanner.close();
    }
}
