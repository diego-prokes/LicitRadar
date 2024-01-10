Proyecto de Automatización de Licitaciones (LicitConcentra)
===========================================================

Descripción
-----------

Este proyecto consiste en un sistema automatizado para extraer información sobre licitaciones de un feed RSS de mercado público, procesar estos datos y luego enviarlos a SharePoint. El sistema está diseñado para facilitar la gestión y el seguimiento de las licitaciones.

Estructura de Archivos
----------------------

*   `licit_tools.py`: Contiene funciones auxiliares para imprimir y procesar la información de las licitaciones.
*   `main.py`: Función principal del programa. Orquesta el proceso de scraping y envío de datos a SharePoint.
*   `scraper.py`: Realiza el scraping de datos del feed RSS de mercado público.
*   `sender.py`: Se encarga de enviar los datos procesados a SharePoint.

Configuración y Uso
-------------------

### Requisitos Previos

*   Python 3.10.13
*   Bibliotecas necesarias: `feedparser`, `requests`, `decouple`, `shareplum`.

### Configuración

1.  Configurar las credenciales de SharePoint y otras configuraciones necesarias en un archivo `.env`.
2.  Asegurarse de que todas las dependencias están instaladas ejecutando `pip install -r requirements.txt` (crear este archivo si es necesario).

### Ejecución

Para ejecutar el programa, simplemente corre `python main.py` desde la línea de comandos.
