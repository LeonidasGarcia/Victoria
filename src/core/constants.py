ACCESS_RAM_COST = 1
PAGE_FAULT_COST = 1000
SWAP_IN_COST = 1000
SWAP_OUT_COST = 1000
RESET_R_COST = 1
RESET_R_INTERVAL = 100

welcome_message = """Victoria es la herramienta definitiva para explorar, visualizar y dominar los fundamentos de la gestión de memoria virtual. Diseñada como un potente simulador, Victoria te permite ir más allá de la teoría al poner a prueba los algoritmos de reemplazo de página más cruciales de los sistemas operativos en un entorno de competencia controlado y analítico.

En Victoria, tú controlas el entorno. Antes de iniciar cualquier competencia, puedes configurar con precisión los siguientes parámetros para modelar cualquier escenario de carga de trabajo:

- Capacidad de Memoria: Define el tamaño de la memoria física disponible, controlando el número de marcos de página a disposición de los procesos.
- Arquitectura del Programa: Ajusta tanto el tamaño total del programa como el tamaño de las páginas individuales para ver cómo la granularidad afecta el rendimiento.
- Rastros de Referencias: La simulación se alimenta de rastros de referencias detallados. Cada solicitud de memoria incluye el ID del programa que la genera, la página solicitada y el modo de acceso (Lectura/Escritura), garantizando una simulación realista del comportamiento de las aplicaciones.
    
El corazón de Victoria es la competición. El simulador está equipado con una selección esencial de estrategias de reemplazo que compiten simultáneamente por los marcos de memoria. Los algoritmos disponibles son:

- Optimal (OPT): Algoritmo dorado
- Least Recently Used (LRU): Estrategia basada en la historia, reemplazando la página que se usó hace más tiempo.
- Not Recently Used (NRU): Utiliza bits de referencia para una aproximación práctica a LRU.
- Second Enhanced Chance (Segunda Oportunidad Mejorada): Una mejora de FIFO que da una "segunda oportunidad" a las páginas que han sido referenciadas.
- First-In, First-Out (FIFO): La estrategia más simple, que reemplaza la página que lleva más tiempo en memoria.
"""
