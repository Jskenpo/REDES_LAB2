import subprocess
import time
import random
import string
import matplotlib.pyplot as plt
import numpy as np
import socket
import sys
import os

def send_receive(message, emisor_port, receptor_port, max_retries=5):
    for _ in range(max_retries):
        try:
            # Enviar al emisor
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect(('localhost', emisor_port))
                s.sendall(message.encode())
                encoded = s.recv(1024).decode()

            # Enviar al receptor
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect(('localhost', receptor_port))
                s.sendall(encoded.encode())
                decoded = s.recv(1024).decode()

            return encoded, decoded
        except (ConnectionRefusedError, socket.timeout):
            print(f"Conexión fallida. Reintentando en 2 segundos...")
            time.sleep(2)
    raise Exception("No se pudo establecer conexión después de varios intentos")

def run_test(num_requests, emisor_port, receptor_port):
    successful_transmissions = 0
    total_bits = 0
    error_bits = 0

    for _ in range(num_requests):
        message = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 20)))
        try:
            encoded, decoded = send_receive(message, emisor_port, receptor_port)
            
            total_bits += len(message) * 7  # 7 bits per ASCII character
            error_bits += sum(a != b for a, b in zip(message, decoded))
            
            if message == decoded:
                successful_transmissions += 1
        except Exception as e:
            print(f"Error en la transmisión: {e}")
            continue

    success_rate = successful_transmissions / num_requests if num_requests > 0 else 0
    bit_error_rate = error_bits / total_bits if total_bits > 0 else 0

    return success_rate, bit_error_rate

def main():
    emisor_port = 5000
    receptor_port = 5001
    error_rates = [0.001, 0.01, 0.05]
    request_counts = [100, 500, 1000]

    # Iniciar el emisor y receptor, redirigiendo su salida
    devnull = open(os.devnull, 'w')
    emisor_process = subprocess.Popen([sys.executable, "Hamming/Hamming.py", str(emisor_port), "0.001"],
                                      stdout=devnull, stderr=devnull)
    receptor_process = subprocess.Popen(["go", "run", "Hamming/Hamming.go", str(receptor_port)],
                                        stdout=devnull, stderr=devnull)

    print("Esperando a que los servidores estén listos...")
    time.sleep(5)

    results = []

    try:
        for error_rate in error_rates:
            # Actualizar la tasa de error del emisor
            emisor_process.terminate()
            emisor_process = subprocess.Popen([sys.executable, "Hamming/Hamming.py", str(emisor_port), str(error_rate)],
                                              stdout=devnull, stderr=devnull)
            time.sleep(2)

            for num_requests in request_counts:
                print(f"Ejecutando prueba con tasa de error {error_rate} y {num_requests} solicitudes...")
                success_rate, bit_error_rate = run_test(num_requests, emisor_port, receptor_port)
                results.append((error_rate, num_requests, success_rate, bit_error_rate))

        # Análisis y visualización de resultados
        error_rates = [r[0] for r in results]
        request_counts = [r[1] for r in results]
        success_rates = [r[2] for r in results]
        bit_error_rates = [r[3] for r in results]

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        for count in set(request_counts):
            plt.plot(
                [r[0] for r in results if r[1] == count],
                [r[2] for r in results if r[1] == count],
                marker='o',
                label=f'{count} requests'
            )
        plt.xlabel('Error Rate')
        plt.ylabel('Success Rate')
        plt.title('Success Rate vs Error Rate')
        plt.legend()

        plt.subplot(1, 2, 2)
        for count in set(request_counts):
            plt.plot(
                [r[0] for r in results if r[1] == count],
                [r[3] for r in results if r[1] == count],
                marker='o',
                label=f'{count} requests'
            )
        plt.xlabel('Error Rate')
        plt.ylabel('Bit Error Rate')
        plt.title('Bit Error Rate vs Error Rate')
        plt.legend()

        plt.tight_layout()
        plt.savefig('hamming_performance.png')
        plt.show()

        # Imprimir estadísticas
        print("\nEstadísticas:")
        for error_rate, num_requests, success_rate, bit_error_rate in results:
            print(f"Tasa de error: {error_rate}, Solicitudes: {num_requests}")
            print(f"  Tasa de éxito: {success_rate:.4f}")
            print(f"  Tasa de error de bits: {bit_error_rate:.6f}")
            print()

    except KeyboardInterrupt:
        print("Prueba interrumpida por el usuario.")
    finally:
        # Cerrar procesos
        print("Cerrando procesos...")
        emisor_process.terminate()
        receptor_process.terminate()
        devnull.close()

if __name__ == "__main__":
    main()