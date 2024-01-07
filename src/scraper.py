import feedparser
import requests
from xml.etree import ElementTree as ET
import re


def scrap_mercado_publico():
    # Url del feed RSS
    rss_url = "https://www.mercadopublico.cl/Portal/feed.aspx?OrgCode=266971"

    # Obtener el contenido del feed RSS
    response = requests.get(rss_url)
    rss_content = response.content

    # Analizar el feed RSS
    feed = feedparser.parse(rss_content)

    # Lista para almacenar las licitaciones que cumplen con ciertas keywords
    licitaciones = []

    # Keywords a buscar en el título y descripción
    keywords = ['aseo clínico', 'aseo industrial', 'bpo', 'candidatos', 'career', 'célula ágil', 'células ágiles',
                'cleaning and disinfection', 'desinfección', 'est', 'excel', 'externalización', 'facility', 'guardias', 'hr',
                'headhunting', 'help desk', 'industrial cleaning', 'it professionals', 'job', 'limpieza y desinfección',
                'limpieza industrial', 'mantenimiento menor', 'mesa de ayuda', 'mesas de ayuda', 'nivelación', 'outsourcing',
                'placement', 'profesional', 'profesionales it', 'psicolaboral', 'psychometrics', 'reclutamiento', 'recruitment',
                'selección', 'servicio temporal', 'servicios temporales', 'servicios transitorios', 'sac', 'seguridad física',
                'soporte', 'staffing', 'talent', 'talent acquisition', 'temporary', 'test de evaluación', 'training',
                'training programs']

    # Iterar sobre los elementos del feed
    for item in feed.entries:
        # extraigo la data
        title = item.title
        description = item.description
        link = item.link
        published = item.published
        # defino mis variables de data
        Id = title.split(" ")[1]
        Titulo = ' '.join(title.split(" ")[3:]).lower()
        Comprador = description.lower().split("<br />")[0][11:]
        Descripcion = description.lower().split("<br />")[1][13:]
        Publicacion = published.split("T")[0]
        Url = link
        # convierto todo a minúsculas
        keywords = [k.lower() for k in keywords]
        # se escapan los caracteres especiales en los keywords para que no afecten las expresiones regulares
        keywords_escaped = [re.escape(k) for k in keywords]
        # se crea un patrón de expresión regular para buscar coincidencias exactas de palabras o frases
        pattern = re.compile(r'\b(?:' + '|'.join(keywords_escaped) + r')\b')
        # Buscamos coincidencias en el título y descripción
        coincidencias = pattern.findall(Titulo)
        coincidencias += pattern.findall(Descripcion)
        # elimino repetidos
        coincidencias = list(set(coincidencias))
        # defino mi última variable de data
        Keywords = coincidencias 
        
        if (published.split("T")[0] == "2024-01-06"): # OJO
            licitacion = {
                "Id"            : Id            ,
                "Titulo"        : Titulo        ,
                "Comprador"     : Comprador     ,
                "Descripcion"   : Descripcion   ,
                "Publicacion"   : Publicacion   ,
                "Url"           : Url           ,
                "Keywords"      : Keywords      ,
            }
            licitaciones.append(licitacion)
    
    return licitaciones


def print_licitaciones(licitaciones):
    # Imprimir las licitaciones 
    for licitacion in licitaciones:
        print("Id           :\t", licitacion["Id"])
        print("Titulo       :\t", licitacion["Titulo"])
        print("Comprador    :\t", licitacion["Comprador"])
        print("Descripcion  :\t", licitacion["Descripcion"])
        print("Publicacion  :\t", licitacion["Publicacion"])
        print("Url          :\t", licitacion["Url"])
        print("Keywords     :\t", licitacion["Keywords"])
        print()

    # Imprimir cuántas licitaciones del día hay
    print(len(licitaciones))


def write_licitaciones(licitaciones):
    licitaciones = scrap_mercado_publico()

    # Crear el elemento raíz del árbol XML
    root = ET.Element("licitaciones")

    for licitacion in licitaciones:
        # Crear un elemento para cada licitación
        licitacion_elem = ET.SubElement(root, "licitacion")
        
        # Agregar subelementos con la información de la licitación
        ET.SubElement(licitacion_elem, "Id").text = licitacion["Id"]
        ET.SubElement(licitacion_elem, "Titulo").text = licitacion["Titulo"]
        ET.SubElement(licitacion_elem, "Comprador").text = licitacion["Comprador"]
        ET.SubElement(licitacion_elem, "Descripcion").text = licitacion["Descripcion"]
        ET.SubElement(licitacion_elem, "Publicacion").text = licitacion["Publicacion"]
        ET.SubElement(licitacion_elem, "Url").text = licitacion["Url"]
        ET.SubElement(licitacion_elem, "Keywords").text = licitacion["Keywords"]

    # Crear un árbol a partir del elemento raíz
    tree = ET.ElementTree(root)

    # Guardar el árbol XML en un archivo
    tree.write("reports/report_mercado_publico.xml")


def main():
    # extraigo las licitaciones del día
    licitaciones = scrap_mercado_publico()

    # las imprimo en la consola
    print_licitaciones(licitaciones)

    # las escribo en un archivo
    # write_licitaciones(licitaciones)


if __name__ == "__main__":
    main()