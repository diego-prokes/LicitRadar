# función para imprimir información sobre las licitaciones
def print_licitaciones(licitaciones):
    # itera sobre cada licitación en la lista
    for licitacion in licitaciones:
        # imprime la información detallada de cada licitación
        print("Id           :\t", licitacion["Id"])
        print("Titulo       :\t", licitacion["Titulo"])
        print("Comprador    :\t", licitacion["Comprador"])
        print("Descripcion  :\t", licitacion["Descripcion"])
        print("Publicacion  :\t", licitacion["Publicacion"])
        print("Url          :\t", licitacion["Url"])
        print("Keywords     :\t", licitacion["Keywords"])
        print()

    # imprime el número total de licitaciones del día
    print(len(licitaciones))

# función para obtener fechas de los últimos n días
def get_dates(n_days=7):
    from datetime import timedelta, date

    dates = []
    # itera para obtener las fechas de los últimos n días
    for i in range(n_days):
        dates.append(str(date.today() - timedelta(days=i)))

    return dates

# función para escribir información de licitaciones en un archivo XML
def write_licitaciones(licitaciones):
    from xml.etree import ElementTree as ET

    # crea el elemento raíz del árbol XML
    root = ET.Element("licitaciones")

    # itera sobre cada licitación en la lista
    for licitacion in licitaciones:
        # crea un elemento para cada licitación
        licitacion_elem = ET.SubElement(root, "licitacion")

        # agrega subelementos con la información de la licitación
        ET.SubElement(licitacion_elem, "Id").text = licitacion["Id"]
        ET.SubElement(licitacion_elem, "Titulo").text = licitacion["Titulo"]
        ET.SubElement(licitacion_elem, "Comprador").text = licitacion["Comprador"]
        ET.SubElement(licitacion_elem, "Descripcion").text = licitacion["Descripcion"]
        ET.SubElement(licitacion_elem, "Publicacion").text = licitacion["Publicacion"]
        ET.SubElement(licitacion_elem, "Url").text = licitacion["Url"]
        ET.SubElement(licitacion_elem, "Keywords").text = licitacion["Keywords"]

    # crea un árbol a partir del elemento raíz
    tree = ET.ElementTree(root)

    # guarda el árbol XML en un archivo
    tree.write("reports/report_mercado_publico.xml")
