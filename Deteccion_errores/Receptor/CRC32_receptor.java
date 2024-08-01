package Receptor;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.zip.CRC32;

public class CRC32_receptor {

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
        try (ServerSocket serverSocket = new ServerSocket(5003)) {
            System.out.println("Receptor CRC-32 esperando conexiones...");
            while (true) {
                try (Socket clientSocket = serverSocket.accept();
                     BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                     OutputStream out = clientSocket.getOutputStream()) {

                    System.out.println("Conexión aceptada de " + clientSocket.getInetAddress());

                    StringBuilder binaryMessage = new StringBuilder();
                    String line;
                    while ((line = in.readLine()) != null && !line.isEmpty()) {
                        System.out.println("Línea recibida: " + line);
                        binaryMessage.append(line);
                    }

                    System.out.println("Mensaje completo recibido: " + binaryMessage.toString());

                    boolean valid = crc32Check(binaryMessage.toString());

                    if (valid) {
                        String messagePart = binaryMessage.substring(0, binaryMessage.length() - 32);
                        try {
                            String message = binaryToString(messagePart);
                            String response = "No se detectaron errores. El mensaje original es: " + message + "\n" +
                                              "Mensaje en binario: " + messagePart + "\n";
                            out.write(response.getBytes());
                            out.flush();  // Asegúrate de vaciar el buffer
                            System.out.println("Respuesta enviada: " + response);
                        } catch (IllegalArgumentException e) {
                            String response = "Error -- convertir binario a string: " + e.getMessage() + "\n";
                            out.write(response.getBytes());
                            out.flush();  // Asegúrate de vaciar el buffer
                            System.out.println("Respuesta enviada: " + response);
                        }
                    } else {
                        String response = "-- Se detectaron errores. Se descarta el mensaje --\n";
                        out.write(response.getBytes());
                        out.flush();  // Asegúrate de vaciar el buffer
                        System.out.println("Respuesta enviada: " + response);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
