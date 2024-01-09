# importa la función 'scrap_mercado_publico' desde el módulo 'scraper'
from scraper import scrap_mercado_publico
# importa la función 'send_to_sharepoint' desde el módulo 'sender'
from sender import send_to_sharepoint

# función principal del programa
def main():
    # llama a la función 'scrap_mercado_publico' para obtener datos de licitaciones
    licitaciones = scrap_mercado_publico()

    # llama a la función 'send_to_sharepoint' para enviar los datos a SharePoint
    send_to_sharepoint(licitaciones)

# verifica si este script está siendo ejecutado directamente
if __name__ == "__main__":
    # si es así, llama a la función 'main' para iniciar la ejecución del programa
    main()
