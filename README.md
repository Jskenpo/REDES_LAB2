
# Algoritmos de detección y corrección: Hamming y CRC-32 

## Algoritmo de Hamming

### Conceptos Básicos

El código Hamming es un método de corrección de errores que permite detectar y corregir errores de bit en la transmisión de datos. Fue inventado por Richard Hamming en 1950.

### Generación de Códigos Hamming

1. **Inserción de Bits de Paridad**: Los bits de paridad se insertan en posiciones específicas de la palabra de datos. Si una palabra de datos tiene `k` bits, se añaden `r` bits de paridad para formar una palabra de código de `n` bits, donde `n = k + r`.
2. **Cálculo de Bits de Paridad**: Los bits de paridad se calculan para cubrir combinaciones específicas de bits en la palabra de código. Cada bit de paridad se coloca en una posición que es una potencia de 2 (1, 2, 4, 8, ...).

### Detección y Corrección de Errores

1. **Recepción y Verificación**: Al recibir una palabra de código, se recalculan los bits de paridad y se comparan con los bits de paridad recibidos.
2. **Identificación de Errores**: Si hay una discrepancia, la posición del bit erróneo se identifica sumando las posiciones de los bits de paridad que no coinciden.
3. **Corrección de Errores**: El bit en la posición identificada se invierte para corregir el error.

## Algoritmo CRC-32

### Conceptos Básicos

CRC (Cyclic Redundancy Check) es un método de detección de errores ampliamente utilizado en redes y sistemas de almacenamiento. CRC-32 utiliza un polinomio de 32 bits para generar un código de redundancia cíclica.

### Generación del CRC

1. **Selección del Polinomio**: Se selecciona un polinomio generador de 32 bits, comúnmente `0x04C11DB7`.
2. **División Polinómica**: Los datos se tratan como coeficientes de un polinomio y se dividen por el polinomio generador utilizando la aritmética binaria (sin acarreo).
3. **Cálculo del Resto**: El resto de esta división es el CRC, que se anexa al final de los datos.

### Verificación del CRC

1. **Recepción de Datos**: Se reciben los datos con el CRC anexado.
2. **División Polinómica**: Se realiza la misma división polinómica sobre los datos recibidos.
3. **Validación del Resto**: Si el resto es cero, los datos se consideran correctos; de lo contrario, se detecta un error.

## Ejecución de código

### Configuración de servidor 

Para probar los algoritmos de Hamming, sigue estos pasos:

1. Abre una terminal.
2. Navega a la carpeta `hamming`
    ```
    cd Hamming 
    ```
3. Ejecuta el archivo del emisor  especificando el puerto y la probabilidad de error `python hamming.py 5000 0.001`
4. Ejecuta el archivo del recepor navegando hacia la direccion donde se encuentra el archivo hamming.go y luego ejecuta el comando `go run .`
5. Dirígete a la carpeta de detección de errores y ejecuta los programas.

Para probar el algoritmo CRC-32, sigue estos pasos:

1. Abre una terminal.
2. Navega en la carpeta `Deteccion_errores`
   ```
    cd Deteccion_errores 
   ```
3.  Ejecuta el archivo del emisor corriendo el programa `CRC-32_emisor.py` para tener listo el servidor
4.  Ejecuta el archivo del emisor corriendo el programa `CRC32_receptor.java` para tener listo el servidor
5.  Dirigete al main y corre el programa

Los puertos por defecto de cada cliente son los siguientes:
- Emisor Hamming: `5000`
- receptor Hamming: `5001`
- Emisor CRC-32: `5002`
- Receptor CRC-32: `5003`

### Módulo principal

**Para poder probar el programa debe de tener ya todos los programas de emisor y receptor ya corriendo**

Puede ejecutar el programa `main.py` mediante uso de la terminal (`python .../main.py`) o usando un IDE en donde podrá probar los distintos algoritmos.

### Pruebas Hamming

#### Funciones Principales

- **`send_receive(message, emisor_port, receptor_port, max_retries=5)`**:
  - Esta función envía un mensaje al emisor y luego al receptor, y recibe la respuesta codificada y decodificada. Reintenta la conexión en caso de fallos.
  
- **`run_test(num_requests, emisor_port, receptor_port)`**:
  - Realiza múltiples pruebas de transmisión de mensajes, calcula la tasa de éxito y la tasa de error de bits, y acumula los resultados para su análisis.
  
- **`main()`**:
  - Configura los puertos del emisor y receptor, inicia los procesos del emisor y receptor, y ejecuta pruebas con diferentes tasas de error y números de solicitudes. Luego, visualiza los resultados y muestra estadísticas.

### Pruebas CRC-32

#### Funciones Principales

- **`send_receive(message,error_rates)`**:
  - Esta función envía un mensaje al emisor y luego al receptor, y recibe la respuesta codificada y decodificada. Reintenta la conexión en caso de fallos. Ademas se le envia la tasa de error que desea utilizar o en caso y no se envie nada, sera default.
  
- **`test_crc32_algorithm(message, error_rates, port_send, port_receive):`**:
  - Realiza múltiples pruebas de transmisión de mensajes, calcula la tasa de éxito y la tasa de error de bits, y acumula los resultados para su análisis.
  
- **`main()`**:
  - Configura los puertos del emisor y receptor, inicia los procesos del emisor y receptor, y ejecuta pruebas con diferentes tasas de error y tamanos del texto binario. Luego, visualiza los resultados y muestra una grafica.
 
- **`plot_results(results)`**:
  - Recibe y almacena los resultados, para despues poder crear graficas que expliquen mejor los mismos resultados.



#### Ejecución del Código

1. **Configuración de los Servidores**:
   - Asegúrate de que los archivos `Hamming.py` (Python) y `Hamming.go` (Go) están disponibles en las carpetas especificadas (`Hamming/`).
   - El archivo `Hamming.py` debe recibir el puerto del emisor y la tasa de error como argumentos.
   - El archivo `Hamming.go` debe escuchar en el puerto del receptor.
   - Asegúrate de que los archivos `CRC-32_emisor.py` (Python) y `CRC32_receptor.java` están disponibles en las carpetas especificadas (`Deteccion_errores/`).
   - El archivo `CRC-32_emisor.py` debe recibir el puerto del emisor.
   - El archivo `CRC32_receptor.java` debe escuchar en el puerto del receptor.

2. **Iniciar el Script**:
   - Ejecuta el archivo Python con el siguiente comando:
     ```bash
     python test2.py
     ```
   - El script iniciará automáticamente los procesos del emisor y receptor, ejecutará las pruebas y visualizará los resultados.

#### Resultados y Visualización

El script genera dos gráficos que muestran:
- La **tasa de éxito** frente a la **tasa de error**.
- La **tasa de error de bits** frente a la **tasa de error**.

Los gráficos se guardan en el archivo `hamming_performance.png` y se muestran al final de la ejecución del script.
Mientras que los resultados del CRC-32 se mostraran al momento y son posibles de guaradar si desea el usuario.

### Requisitos

- **Python 3.x**: Para ejecutar el script principal.
- **Go**: Para ejecutar el archivo `Hamming.go`.
- **Matplotlib**: Para generar gráficos (instalar con `pip install matplotlib`).
- **Numpy**: Requerido para el manejo de datos (instalar con `pip install numpy`).


