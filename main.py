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
    licitaciones_interesantes = []

    # Keywords a buscar en el título o comprador
    keywords = ["servicio", "vigilancia", "seguridad"]

    # Iterar sobre los elementos del feed
    for item in feed.entries:
        title = item.title
        description = item.description
        link = item.link
        published = item.published

        # Verificar si alguna keyword está en el título o comprador
        if any(keyword.lower() in title.lower() or keyword.lower() in description.lower() for keyword in keywords):
            # Guardar la información de la licitación
            licitacion = {
                "Id": title.split(" ")[1],
                "Nombre": ' '.join(title.split(" ")[3:]).lower(),
                "Comprador": description.lower().split("<br />")[0][11:],
                "Descripcion": description.lower().split("<br />")[1][13:],
                "Publicación": published.split("T")[0],
                "Url": link
            }
            licitaciones_interesantes.append(licitacion)

    # Imprimir las licitaciones que cumplen con las keywords
    for licitacion in licitaciones_interesantes:
        print("Id           :\t", licitacion["Id"])
        print("Nombre       :\t", licitacion["Nombre"])
        print("Comprador    :\t", licitacion["Comprador"])
        print("Descripcion  :\t", licitacion["Descripcion"])
        print("Publicación  :\t", licitacion["Publicación"])
        print("Url          :\t", licitacion["Url"])
        print()

    
    # (Aquí iría el código para enviar las licitaciones a SharePoint)



if __name__ == "__main__":
    main()