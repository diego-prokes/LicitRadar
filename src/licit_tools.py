# Imprimir las licitaciones 
def print_licitaciones(licitaciones):
    
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

def get_dates(n_days=7):

    from datetime import timedelta
    from datetime import date

    dates = []
    for i in range(n_days):
        dates.append(str(date.today()-timedelta(days=i)))

    return dates

def write_licitaciones(licitaciones):

    from xml.etree import ElementTree as ET

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