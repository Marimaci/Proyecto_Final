import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import re

def imagenes(busqueda, paginas):
    s = Service(ChromeDriverManager().install())
    opc = Options()
    opc.add_argument("--window.size=1020,1200")
    navegador = webdriver.Chrome(service=s, options=opc)

    navegador.get("https://www.amazon.com.mx/")
    time.sleep(5)
    txtInput = navegador.find_element(By.ID, value="twotabsearchtextbox")
    txtInput.send_keys(busqueda)
    txtInput.submit()

    data = {"Titulo": [], "Precio": [], "Valoracion": [], "Precio_sin_descuento": [], "Tienda": [],
            "Marca": []}  # Agregada columna "Marca"
    marcas = ["Samsung", "Iphone", "Motorola", "Redmi", "Oppo", "Xiaomi", "Moto"]

    for page in range(paginas):
       time.sleep(5)
       navegador.save_screenshot(f"imaga/{busqueda}_{page}.png")
       soup = BeautifulSoup(navegador.page_source, features="html5lib")
       productos = soup.find_all("div", attrs={
           "class": "a-section a-spacing-small puis-padding-left-small puis-padding-right-small"})

       for item in productos:
           titulo = item.find("span", attrs={"class": "a-size-base-plus a-color-base a-text-normal"})
           precio = item.find("span", attrs={"class": "a-price-whole"})
           valoracion = item.find("span", attrs={"class": "a-icon-alt"})

          # Buscando el precio original (descuento)
           descuento = item.find("div",
                                 attrs={"class": "a-section aok-inline-block"})  # Clase para precio original (tachado)

          # Titulo
           if titulo:
               titulo_texto = titulo.text
               data["Titulo"].append(titulo_texto)
           else:
               data["Titulo"].append("Sin título")

          # Precio
           if precio:
               data["Precio"].append(precio.text)
           else:
               data["Precio"].append(None)

          # Valoracion
           if valoracion:
               data["Valoracion"].append(valoracion.text)
           else:
               data["Valoracion"].append(None)

          # Descuento (precio original)
           if descuento:
              # Extraemos solo el precio sin el texto "Precio de lista:"
               precio_sin_descuento = descuento.find("span", class_="a-offscreen")
               if precio_sin_descuento:
                   descuento_texto = precio_sin_descuento.text.strip()  # Limpiar el texto del precio
                   data["Precio_sin_descuento"].append(descuento_texto)
               else:
                   data["Precio_sin_descuento"].append(None)
           else:
               data["Precio_sin_descuento"].append(None)

          # Tienda
           data["Tienda"].append('amazon')

          # Marca: Buscar si el título contiene alguna de las marcas especificadas
           marca_encontrada = None
           for marca in marcas:
               if marca.lower() in titulo_texto.lower():
                   marca_encontrada = marca
                   break  # Si se encuentra una marca, salir del bucle
           if marca_encontrada:
               data["Marca"].append(marca_encontrada)
           else:
               data["Marca"].append("Desconocida")

    bottonSiguiente = navegador.find_element(By.LINK_TEXT, value="Siguiente")
    bottonSiguiente.click()

    for i in range(len(data["Marca"])):
        if data["Marca"][i] == "Moto":
            data["Marca"][i] = "Motorola"

    time.sleep(5)
    navegador.quit()

    df = pd.DataFrame(data)
    df.to_csv("database/celulares_amazon2.csv", index_label="ID")  # Guardamos el CSV con índice ID

if __name__ == "__main__":
    busqueda = "celulares"
    paginas = 6
    imagenes(busqueda, paginas)


#-------------------------------------------------------------------------------


 #archivo1 = "database/celulares_amazon2.csv"
 #archivo2 = "database/celulares_merc2.csv"


 #procesar_archivos(archivo1, archivo2)


#-------------------------------------------------------------------------------

"""
    datos = combinar_datos("database/amazon_10.csv", "database/mercado_3.csv")
    if datos is not None:
        print(datos.head())
"""