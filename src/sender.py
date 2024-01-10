# Importaciones
from decouple import config
from shareplum import Site, Office365
from shareplum.site import Version
from licit_tools import print_licitaciones, read_xml_to_dict

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
    list_ids = sharepoint_list.GetListItems(fields=["Id","ID"])
    f_list_ids = [fli["Id"] for fli in list_ids]

    # Prepara la data para ser enviada
    send_licitaciones = [licitacion for licitacion in licitaciones if licitacion["Id"] not in f_list_ids]

    print("Licitaciones Enviadas:")
    print_licitaciones(send_licitaciones)

    # if send_licitaciones:
    #     sharepoint_list.UpdateListItems(data=send_licitaciones, kind="New")
    # else:
    #     print("No hay licitaciones nuevas")

if __name__ == "__main__":
    # Retorna una lista de diccionarios con el reporte de prueba desde el archivo XML
    licitaciones = read_xml_to_dict("reports/report_mercado_publico.xml")

    # Envía la información a SharePoint
    send_to_sharepoint(licitaciones)
