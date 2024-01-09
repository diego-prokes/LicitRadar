# Importaciones
from scraper import scrap_mercado_publico
from sender import send_to_sharepoint

# Función principal del programa
def main():
    """
    Función principal del programa que realiza scraping de datos y los envía a SharePoint.
    """
    # Llama a la función 'scrap_mercado_publico' para obtener datos de licitaciones
    licitaciones = scrap_mercado_publico()

    # Llama a la función 'send_to_sharepoint' para enviar los datos a SharePoint
    send_to_sharepoint(licitaciones)

# Verifica si este script está siendo ejecutado directamente
if __name__ == "__main__":
    # Si es así, llama a la función 'main' para iniciar la ejecución del programa
    main()

