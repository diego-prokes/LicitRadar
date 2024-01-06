def main():
    import feedparser
    import requests
    from xml.etree import ElementTree as ET

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
                'cleaning and disinfection', 'desinfección', 'est', 'excel', 'externalización', 'facility', 'guardias' 'hr',
                'headhunting', 'help desk', 'industrial cleaning', 'it professionals', 'job', 'limpieza y desinfección',
                'limpieza industrial', 'mantenimiento menor', 'mesa de ayuda', 'mesas de ayuda', 'nivelación', 'outsourcing',
                'placement', 'profesional', 'profesionales it', 'psicolaboral', 'psychometrics', 'reclutamiento', 'recruitment',
                'selección', 'servicio temporal', 'servicios temporales', 'servicios transitorios', 'sac', 'seguridad física',
                'soporte', 'staffing', 'talent', 'talent acquisition', 'temporary', 'test de evaluación', 'training',
                'training programs']

    # Iterar sobre los elementos del feed
    for item in feed.entries:
        title = item.title
        description = item.description
        link = item.link
        published = item.published
        appearing_keywords = []
        for keyword in keywords:
            if keyword.lower() in title.lower() or keyword.lower() in description.lower():
                appearing_keywords.append(keyword)
        licitacion = {
            "Id": title.split(" ")[1],
            "Titulo": ' '.join(title.split(" ")[3:]).lower(),
            "Comprador": description.lower().split("<br />")[0][11:],
            "Descripcion": description.lower().split("<br />")[1][13:],
            "Publicacion": published.split("T")[0],
            "Url": link,
            "Keywords": ', '.join(appearing_keywords),
        }
        licitaciones.append(licitacion)

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




    
    # Aquí va el código para enviar las licitaciones a SharePoint

    # send to sharepoint process
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

    # # descargo los títulos de la lista de sharepoint
    # until_now_data = list.GetListItems(fields=["Título"])
    # f_until_now_data = []
    # for und in until_now_data:
    #     f_until_now_data.append(und["Título"])

    # print(f_until_now_data)

    # actualizo la lista



    # print(licitaciones_interesantes)

    if licitaciones != []:
        list.UpdateListItems(data=licitaciones, kind="New")
    else:
        print("No hay licitaciones interesantes")

if __name__ == "__main__":
    main()