def main():
    from scraper import scrap_mercado_publico
    from sender import send_to_sharepoint

    licitaciones = scrap_mercado_publico()
    
    send_to_sharepoint(licitaciones)

if __name__ == "__main__":
    main()