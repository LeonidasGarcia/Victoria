# Proyecto: Victoria - Simulador de Gestión de Memoria Virtual

## 1. Introducción al Proyecto

**Victoria** es una herramienta educativa e interactiva diseñada para explorar, visualizar y dominar los fundamentos de la gestión de memoria virtual. Los sistemas operativos modernos utilizan la memoria virtual para ejecutar programas más grandes que la memoria física disponible y para proporcionar aislamiento entre procesos. La piedra angular de este sistema es el mecanismo de **paginación por demanda** y, cuando la memoria se llena, el **algoritmo de reemplazo de página**.

Este simulador permite ir más allá de la teoría abstracta al poner a prueba los algoritmos de reemplazo de página más cruciales en un entorno de competencia controlado y analítico. Victoria permite a los usuarios configurar un entorno de memoria, definir una carga de trabajo (traza de referencias) y observar visualmente cómo cada algoritmo toma decisiones y cuál ofrece el mejor rendimiento.

## 2. Características Principales

El simulador está construido con una robusta lógica de simulación en Python y una interfaz gráfica de usuario (GUI) desarrollada con Tkinter.

* **Comparación Simultánea:** La plataforma permite ejecutar múltiples algoritmos de reemplazo de página en paralelo (lado a lado), utilizando exactamente la misma traza de referencias de memoria. Esto facilita una comparación directa y justa de su rendimiento y comportamiento bajo la misma carga de trabajo.

* **Entorno Altamente Configurable:** Los usuarios pueden definir con precisión los parámetros clave del sistema antes de iniciar la simulación a través de un formulario dedicado:
    * **Tamaño de Memoria RAM:** Define la cantidad total de memoria física disponible para los marcos de página.
    * **Tamaño de Programa:** Establece el tamaño del espacio de direcciones virtual de los programas.
    * **Tamaño de Página/Marco:** Define el tamaño de cada página virtual y marco de página físico. El sistema valida que la RAM y el tamaño del programa sean múltiplos enteros del tamaño de página.
    * **Número de Programas (Procesos):** Especifica cuántos procesos distintos participarán en la simulación.

* **Gestión de Trazas de Referencia:** El simulador se alimenta de una traza de referencias que simula la carga de trabajo. Los usuarios pueden crear esta traza manualmente, entrada por entrada:
    * Cada referencia especifica el **ID del programa (PID)** que realiza el acceso.
    * La **página virtual (VPN)** solicitada.
    * El **modo de acceso** (Lectura 'r' o Escritura 'w'), que es crucial para manejar el "bit de modificación" (dirty bit).

* **Sistema de Presets (Preajustes):** Para facilitar las pruebas y demostraciones, Victoria puede guardar y cargar configuraciones completas de simulación. Estos "presets" almacenan los parámetros de memoria y las trazas de referencia completas en archivos CSV (`presets.csv` y `presets_reference_trace.csv`), permitiendo reutilizar escenarios complejos fácilmente.

* **Visualización Detallada en Tiempo Real:** Cada algoritmo seleccionado se ejecuta en su propia "Celda Victoria" (`VictoriaCell`). Esta celda muestra:
    * El estado actual de la memoria RAM, mostrando qué marco está ocupado y por qué programa.
    * La lista de programas (procesos) cargados en la simulación.
    * La solicitud de memoria que se está procesando actualmente.
    * Un panel de métricas de rendimiento actualizado en vivo.

* **Generación Aleatoria:** Para pruebas rápidas, la aplicación puede generar una configuración de memoria, programas y una traza de referencias aleatoria con un solo clic.

## 3. El Núcleo del Simulador: ¿Cómo funciona?

El motor de simulación (`Victoria` en `src/core/victoria.py`) es el corazón del proyecto. Opera procesando secuencialmente cada solicitud de la traza de referencias para cada algoritmo seleccionado.

1.  **Gestión del Reloj:** Se mantiene un **reloj lógico** que avanza con cada operación (acceso a RAM, fallo de página, swap-in, swap-out). Este reloj es fundamental para el costo de las operaciones y para el funcionamiento de algoritmos como LRU (que rastrea el `referenced_time`) y para el reseteo periódico de bits 'R' en NRU y Reloj.

2.  **Búsqueda en Tabla de Páginas (Page Table Hit):** Cuando se procesa una referencia (`PID`, `VPN`, `modo`), el simulador primero consulta la **tabla de páginas** (`PageTable`) de ese proceso.
    * Si la página es válida (bit de validez = 1), es un **"Page Hit"**.
    * Se actualiza el `referenced_time` del marco y se establece el bit de Referencia (R) en 1.
    * Si el modo es 'w' (escritura), se establece el bit de Modificación (M) o "dirty bit" en 1.

3.  **Manejo de Fallo de Página (Page Fault):** Si la página no es válida (bit de validez = 0), se produce un **"Page Fault"**, y se incrementa el contador de fallos.
    * El simulador primero busca un marco de página libre (`pid == -1`) en el gestor de RAM.
    * **Si hay un marco libre:** La página se carga directamente en ese marco (ver "Swap-In").
    * **Si no hay marcos libres:** Se debe seleccionar una víctima.

4.  **Selección de Víctima:** El simulador invoca al **algoritmo de reemplazo de página** (`PageReplacementAlgorithm`) que tiene asignado.
    * El algoritmo (LRU, FIFO, etc.) analiza el estado de todos los marcos de página (almacenado en un DataFrame de `pandas` en `RamManager`) y elige un marco "víctima" para ser desalojado, devolviendo su FPN (Frame Page Number).

5.  **Swap-Out (Página Sucia):** Una vez seleccionada la víctima, el simulador consulta su bit 'M' (dirty).
    * Si la página víctima está "sucia" (bit 'M' = 1), significa que fue modificada y debe ser "guardada" en disco. Se simula una operación de **Swap-Out**, que añade un costo significativo al reloj lógico.
    * La tabla de páginas del proceso víctima se actualiza para invalidar esa página.

6.  **Swap-In:** Finalmente, la página que originalmente causó el fallo se "carga" en el marco de página ahora libre.
    * Se simula una operación de **Swap-In** (ya sea desde disco o cargada por primera vez), añadiendo otro costo al reloj.
    * La tabla de páginas del proceso solicitante se actualiza, vinculando su VPN al FPN recién ocupado y marcándola como válida.

## 4. Algoritmos Implementados

Victoria incluye implementaciones de los algoritmos de reemplazo de página más fundamentales:

* **Optimal (OPT):** El algoritmo teórico perfecto. Mira hacia el *futuro* en la traza de referencias y elige la página que tardará más tiempo en volver a ser usada. Sirve como la línea base ideal de rendimiento.
* **Least Recently Used (LRU):** Mira hacia el *pasado*. Reemplaza la página que no ha sido usada por la mayor cantidad de tiempo (busca el `referenced_time` más antiguo).
* **First-In, First-Out (FIFO):** El algoritmo más simple. Reemplaza la página que lleva más tiempo en memoria (busca el `load_time` más antiguo).
* **Not Recently Used (NRU):** Un algoritmo de aproximación a LRU que utiliza los bits de Referencia (R) y Modificación (M) para clasificar las páginas en cuatro categorías y elige una víctima de la categoría más baja.
* **Reloj (CLK / Segunda Oportunidad):** Una mejora de FIFO que usa un puntero (manecilla de reloj) y el bit de Referencia (R) para dar una "segunda oportunidad" a las páginas que han sido usadas recientemente.

## 5. Métricas de Rendimiento

El objetivo principal de la simulación es analizar el rendimiento. La clase `Metrics` rastrea y calcula las siguientes estadísticas clave, que se muestran en la GUI:

* **Tiempo Lógico (Logic Time):** El costo total en "unidades de tiempo" simuladas para procesar la traza.
* **Conteo de Fallos de Página (PF Count):** El número total de veces que se requirió una página que no estaba en RAM.
* **Tasa de Fallos de Página (PF Rate):** El porcentaje de accesos a memoria que resultaron en un fallo de página.
* **Tiempo Promedio de Acceso (AVG Time Access):** El costo promedio de cada acceso a memoria (Tiempo Lógico / Total de Accesos).
* **Uso de Memoria (Memory Usage):** El porcentaje de marcos de página que están actualmente ocupados.
