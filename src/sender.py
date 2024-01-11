# Importaciones
from decouple import config
from shareplum import Site, Office365
from shareplum.site import Version
from licit_tools import print_licitaciones, read_xml_to_dict

def send_to_sharepoint(licitaciones):
    """
    Envía las licitaciones a SharePoint si no existen previamente en la lista especificada.
    """
    print("Realizando conexión a SharePoint")
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
    list_ids = sharepoint_list.GetListItems(fields=["Id", "ID"])
    dict_ids = {aux["Id"]: aux["ID"] for aux in list_ids}

    # Preparar datos para actualización o creación
    print("Preparando las licitaciones para ser enviada\n")
    licitaciones_para_actualizar = []
    licitaciones_para_crear = []

    for licitacion in licitaciones:
        if licitacion["Id"] in dict_ids:
            # La licitación existe, preparar para actualizar
            # Agregar el ID de SharePoint necesario para la actualización
            licitacion["ID"] = dict_ids[licitacion["Id"]]
            licitaciones_para_actualizar.append(licitacion)
        else:
            # La licitación es nueva, preparar para crear
            licitaciones_para_crear.append(licitacion)

    print("Enviando las licitaciones a sharepoint")
    # Procesar las actualizaciones
    if licitaciones_para_actualizar:
        sharepoint_list.UpdateListItems(data=licitaciones_para_actualizar, kind="Update")

    # Procesar las nuevas creaciones
    if licitaciones_para_crear:
        sharepoint_list.UpdateListItems(data=licitaciones_para_crear, kind="New")
        print("Licitaciones Nuevas Enviadas:")
        print_licitaciones(licitaciones_para_crear)

    print(f"Se han extraído: {len(licitaciones)} licitaciones")
    print(f"Se han actualizado: {len(licitaciones_para_actualizar)} licitaciones")
    print(f"Se han creado: {len(licitaciones_para_crear)} licitaciones")



if __name__ == "__main__":
    # Retorna una lista de diccionarios con el reporte de prueba desde el archivo XML
    licitaciones = read_xml_to_dict("reports/report_mercado_publico.xml")

    # Envía la información a SharePoint
    send_to_sharepoint(licitaciones)
