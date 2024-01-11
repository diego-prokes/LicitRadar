# Función para imprimir información sobre las licitaciones
def print_licitaciones(licitaciones):
    '''
    Imprime información detallada sobre cada licitación en la lista proporcionada.

    Parámetros:
    licitaciones (list): Lista de diccionarios, donde cada diccionario contiene detalles de una licitación.

    Esta función itera sobre cada licitación en la lista, imprimiendo los detalles como Id, Título, Comprador, etc.
    '''
    # Itera sobre cada licitación en la lista
    for licitacion in licitaciones:
        # Imprime la información detallada de cada licitación
        print(f"Id           : {licitacion['Id']}")
        print(f"Titulo       : {licitacion['Titulo']}")
        print(f"Comprador    : {licitacion['Comprador']}")
        print(f"Descripcion  : {licitacion['Descripcion']}")
        print(f"Publicacion  : {licitacion['Publicacion']}")
        print(f"Url          : {licitacion['Url']}")
        print(f"Keywords     : {licitacion['Keywords']}")
        print()

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

def read_xml_to_dict(xml_file):
    """
    Lee un archivo XML y retorna una lista de diccionarios con la información de licitaciones.
    """
    import xml.etree.ElementTree as ET

    tree = ET.parse(xml_file)
    root = tree.getroot()

    licitaciones = []

    for licitacion_elem in root.findall('licitacion'):
        licitacion = {
            "Id": licitacion_elem.find('Id').text,
            "Titulo": licitacion_elem.find('Titulo').text,
            "Comprador": licitacion_elem.find('Comprador').text,
            "Descripcion": licitacion_elem.find('Descripcion').text,
            "Publicacion": licitacion_elem.find('Publicacion').text,
            "Url": licitacion_elem.find('Url').text,
            "Keywords": licitacion_elem.find('Keywords').text,
        }
        licitaciones.append(licitacion)

    return licitaciones
