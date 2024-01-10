# Importaciones
from licit_tools import get_dates, print_licitaciones, write_licitaciones
import feedparser
import requests
import re
import json

def scrap_mercado_publico():
    '''
    Función que realiza scrapping al feed RSS de mercado público y retorna las licitaciones
    que cumplen con ciertas palabras clave.
    '''
    try:
        # Obtener las fechas de los últimos <n_days> días utilizando la función get_dates
        n_days = 7
        dates = get_dates(n_days)

        # URL del feed RSS de mercado público
        rss_url = "https://www.mercadopublico.cl/Portal/feed.aspx?OrgCode=266971"

        # Obtener el contenido del feed RSS
        response = requests.get(rss_url)
        rss_content = response.content

        # Guardar el feed RSS parseado
        feed = feedparser.parse(rss_content)

        # Lista para almacenar las licitaciones que cumplen con ciertas palabras clave
        licitaciones = []

        # Palabras clave a buscar en el título y descripción de las licitaciones
        with open('kw_mercado_publico.json', 'r') as config_file:
            config_data = json.load(config_file)

        keywords = config_data.get('keywords', [])

        # Iterar sobre los elementos del feed
        for item in feed.entries:
            # Extraer la información relevante de cada licitación
            title = item.title
            description = item.description
            link = item.link
            published = item.published

            # Definir variables de datos
            Id = title.split(" ")[1]
            Titulo = ' '.join(title.split(" ")[3:]).lower()
            Comprador = description.lower().split("<br />")[0][11:]
            Descripcion = description.lower().split("<br />")[1][13:]
            Publicacion = published.split("T")[0]
            Url = link

            # Convertir todas las palabras clave a minúsculas
            keywords_lower = [k.lower() for k in keywords]

            # Escapar caracteres especiales en las palabras clave
            keywords_escaped = [re.escape(k) for k in keywords_lower]

            # Crear un patrón de expresión regular para buscar coincidencias exactas de palabras o frases
            pattern = re.compile(r'\b(?:' + '|'.join(keywords_escaped) + r')\b')

            # Buscar coincidencias en el título y descripción
            coincidencias = pattern.findall(Titulo)
            coincidencias += pattern.findall(Descripcion)

            # Eliminar duplicados de coincidencias
            coincidencias = list(set(coincidencias))

            # Definir la variable de datos final
            Keywords = ', '.join(coincidencias)

            # Verificar si la fecha de publicación está en el rango de fechas de interés
            if Publicacion in dates:
                licitacion = {
                    "Id": Id,
                    "Titulo": Titulo,
                    "Comprador": Comprador,
                    "Descripcion": Descripcion,
                    "Publicacion": Publicacion,
                    "Url": Url,
                    "Keywords": Keywords,
                }
                licitaciones.append(licitacion)
    except requests.exceptions.RequestException as e:
        print(f"Error en la operación de red: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    return licitaciones

def main():
    """
    Función principal para realizar pruebas y ejecutar el programa.
    """
    # Extraer las licitaciones del día
    licitaciones = scrap_mercado_publico()

    # Escribir las licitaciones en un archivo XML
    write_licitaciones(licitaciones)

if __name__ == "__main__":
    # Llamar a la función principal si el script se ejecuta directamente
    main()
