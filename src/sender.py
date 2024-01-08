def send_to_sharepoint(licitaciones):

    from decouple import config
    from shareplum import Site
    from shareplum import Office365
    from shareplum.site import Version

    # credenciales de sharepoint
    creds = {
        "username"  :   config('SP_USERNAME'), 
        "password"  :   config('SP_PASSWORD') 
    }
    
    # info de la url de la página de sharepoint
    site_info = {
        'url_base'  :   config('SP_URL_BASE'),
        'site_name' :   config('SP_SITE_NAME'),
        'list_name' :   config('SP_LIST_NAME')
    }
    
    # conexión a la página de sharepoint
    dir = {'url_base':site_info['url_base'], 'site_name':site_info['site_name']}
    try:
        authcookie = Office365(dir['url_base'], username=creds["username"], password=creds["password"]).GetCookies()
        site = Site(f"{dir['url_base']}/sites/{dir['site_name']}", version=Version.v2019, authcookie=authcookie)
    except:
        print("FAILED")

    # conexión a la lista de sharepoint que quiero actualizar
    list = site.List(site_info['list_name'])

    # descargo los Id de la lista de sharepoint
    list_ids = list.GetListItems(fields=["Id"])
    f_list_ids = []
    for fli in list_ids:
        f_list_ids.append(fli["Id"])

    # preparo la data para ser enviada
    send_licitaciones = []
    for licitacion in licitaciones:
        if licitacion["Id"] not in f_list_ids:
            send_licitaciones.append(licitacion)

    print("Licitaciones Enviadas:")
    print_licitaciones(send_licitaciones)

    if send_licitaciones != []:
        list.UpdateListItems(data=send_licitaciones, kind="New")
    else:
        print("No hay licitaciones interesantes")

def read_xml_to_dict(xml_file):

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

if __name__ == "__main__":
    # retorna una lista de diccionarios con el reporte de prueba
    licitaciones = read_xml_to_dict("reports/report_mercado_publico.xml")

    # # imprimo el diccionario de licitaciones
    # print_licitaciones(licitaciones)
    
    # envío la info a sharepoint
    send_to_sharepoint(licitaciones)