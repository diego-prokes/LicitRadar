# función que hace scrap al feed rss de mercado publico
def scrap_mercado_publico():

    from licit_tools import get_dates
    import feedparser
    import requests
    import re

    # obtengo las fechas de los últimos <n_days> días
    n_days = 7
    dates = get_dates(n_days)

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
    keywords = ['aseo', 'aseo clínico', 'aseo industrial', 'bpo', 'candidatos', 'career', 'célula ágil', 'células ágiles',
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
        Keywords = ', '.join(coincidencias)
        
        # si la fecha de publicación está en el rango de fechas que me interesa:
        if (Publicacion in dates): # OJO
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


def main():

    from licit_tools import print_licitaciones, write_licitaciones

    # extraigo las licitaciones del día
    licitaciones = scrap_mercado_publico()

    # las imprimo en la consola
    print_licitaciones(licitaciones)

    # las escribo en un archivo
    write_licitaciones(licitaciones)


if __name__ == "__main__":
    main()