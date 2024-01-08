import feedparser
import requests
from xml.etree import ElementTree as ET
from scraper import scrap_mercado_publico
from sender import send_to_sharepoint
def main():

    licitaciones = scrap_mercado_publico()
    
    send_to_sharepoint(licitaciones)

if __name__ == "__main__":
    main()