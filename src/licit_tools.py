# Función para imprimir información sobre las licitaciones
def print_licitaciones(licitaciones):
    """
    Imprime información detallada sobre cada licitación y el número total de licitaciones del día.
    """
    # Itera sobre cada licitación en la lista
    for licitacion in licitaciones:
        # Imprime la información detallada de cada licitación
        print("Id           :\t", licitacion["Id"])
        print("Titulo       :\t", licitacion["Titulo"])
        print("Comprador    :\t", licitacion["Comprador"])
        print("Descripcion  :\t", licitacion["Descripcion"])
        print("Publicacion  :\t", licitacion["Publicacion"])
        print("Url          :\t", licitacion["Url"])
        print("Keywords     :\t", licitacion["Keywords"])
        print()

    # Imprime el número total de licitaciones del día
    print(len(licitaciones))

# Función para obtener fechas de los últimos n días
def get_dates(n_days=7):
    """
    Retorna una lista de fechas para los últimos n días.
    """
    # Importaciones
    from datetime import timedelta, date

    dates = []
    # Itera para obtener las fechas de los últimos n días
    for i in range(n_days):
        dates.append(str(date.today() - timedelta(days=i)))

    return dates

# Función para escribir información de licitaciones en un archivo XML
def write_licitaciones(licitaciones):
    """
    Escribe la información de licitaciones en un archivo XML.
    """
    # Importaciones
    from xml.etree import ElementTree as ET

    # Crea el elemento raíz del árbol XML
    root = ET.Element("licitaciones")

    # Itera sobre cada licitación en la lista
    for licitacion in licitaciones:
        # Crea un elemento para cada licitación
        licitacion_elem = ET.SubElement(root, "licitacion")

        # Agrega subelementos con la información de la licitación
        ET.SubElement(licitacion_elem, "Id").text = licitacion["Id"]
        ET.SubElement(licitacion_elem, "Titulo").text = licitacion["Titulo"]
        ET.SubElement(licitacion_elem, "Comprador").text = licitacion["Comprador"]
        ET.SubElement(licitacion_elem, "Descripcion").text = licitacion["Descripcion"]
        ET.SubElement(licitacion_elem, "Publicacion").text = licitacion["Publicacion"]
        ET.SubElement(licitacion_elem, "Url").text = licitacion["Url"]
        ET.SubElement(licitacion_elem, "Keywords").text = licitacion["Keywords"]

    # Crea un árbol a partir del elemento raíz
    tree = ET.ElementTree(root)

    # Guarda el árbol XML en un archivo
    tree.write("reports/report_mercado_publico.xml")
