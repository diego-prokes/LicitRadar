from decouple import config
from shareplum import Site, Office365
from shareplum.site import Version

def send_to_sharepoint(licitaciones):
    """
    Envía las licitaciones a SharePoint si no existen previamente en la lista especificada.
    """
    # Credenciales de SharePoint
    creds = {
        "username": config('SP_USERNAME'),
        "password": config('SP_PASSWORD')
    }
    
    # Información de la URL de la página de SharePoint
    site_info = {
        'url_base': config('SP_URL_BASE'),
        'site_name': config('SP_SITE_NAME'),
        'list_name': config('SP_LIST_NAME')
    }
    
    # Conexión a la página de SharePoint
    dir = {'url_base': site_info['url_base'], 'site_name': site_info['site_name']}
    try:
        authcookie = Office365(dir['url_base'], username=creds["username"], password=creds["password"]).GetCookies()
        site = Site(f"{dir['url_base']}/sites/{dir['site_name']}", version=Version.v2019, authcookie=authcookie)
    except:
        print("FAILED")

    # Conexión a la lista de SharePoint que se desea actualizar
    sharepoint_list = site.List(site_info['list_name'])

    # Descarga los IDs de la lista de SharePoint
    list_ids = sharepoint_list.GetListItems(fields=["Id"])
    f_list_ids = [fli["Id"] for fli in list_ids]

    # Prepara la data para ser enviada
    send_licitaciones = [licitacion for licitacion in licitaciones if licitacion["Id"] not in f_list_ids]

    print("Licitaciones Enviadas:")
    print_licitaciones(send_licitaciones)

    if send_licitaciones:
        sharepoint_list.UpdateListItems(data=send_licitaciones, kind="New")
    else:
        print("No hay licitaciones interesantes")

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

def print_licitaciones(licitaciones):
    """
    Imprime información detallada sobre cada licitación.
    """
    for licitacion in licitaciones:
        print("Id           :\t", licitacion["Id"])
        print("Titulo       :\t", licitacion["Titulo"])
        print("Comprador    :\t", licitacion["Comprador"])
        print("Descripcion  :\t", licitacion["Descripcion"])
        print("Publicacion  :\t", licitacion["Publicacion"])
        print("Url          :\t", licitacion["Url"])
        print("Keywords     :\t", licitacion["Keywords"])
        print()

if __name__ == "__main__":
    # Retorna una lista de diccionarios con el reporte de prueba desde el archivo XML
    licitaciones = read_xml_to_dict("reports/report_mercado_publico.xml")

    # Imprime el diccionario de licitaciones (comentado para evitar imprimir en cada ejecución)
    # print_licitaciones(licitaciones)

    # Envía la información a SharePoint
    send_to_sharepoint(licitaciones)
