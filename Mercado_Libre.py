import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd




def web_scraping(busqueda, paginas):
 s = Service(ChromeDriverManager().install())
 opc = Options()
 opc.add_argument("--window.size=1020,1200")
 navegador = webdriver.Chrome(service=s, options=opc)




 navegador.get("https://www.mercadolibre.com.mx/")
 time.sleep(5)
 txtInput = navegador.find_element(By.ID, value="cb1-edit")
 txtInput.send_keys(busqueda)
 txtInput.submit()




 data = {"Titulo": [], "Precio": [], "Valoracion": [], "Precio_sin_descuento": [], "Tienda": [], "Marca": []}  # Agregada columna "Marca"
 marcas = ["Samsung", "Iphone", "Motorola", "Redmi", "Oppo", "Xiaomi", "Moto"]




 for page in range(paginas):
     time.sleep(5)


     try:
         #Hacer clic en el botón de aceptar cookies y asi evitar errores al dar clic en el boton siguiente
         if page == 0:
             aceptar_cookies = navegador.find_element(By.CLASS_NAME,"cookie-consent-banner-opt-out__action--key-accept")
             aceptar_cookies.click()
             time.sleep(2)
     except:
         print("No se encontró el banner de cookies o ya estaba cerrado")




     soup = BeautifulSoup(navegador.page_source, features="html5lib")
     productos = soup.find_all("div", attrs={
         "class": "poly-card__content"})




     for item in productos:
         titulo = item.find("h2", attrs={"class": "poly-box poly-component__title"})
         precio = item.find("span", attrs={"class": "andes-money-amount andes-money-amount--cents-superscript"})
         valoracion = item.find("span", attrs={"class": "andes-visually-hidden"})




         # Buscando el precio original (descuento)
         descuento = item.find("s", attrs=
             {"class": "andes-money-amount andes-money-amount--previous andes-money-amount--cents-dot"})




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
             data["Precio_sin_descuento"].append(descuento.text)
         else:
             data["Precio_sin_descuento"].append(None)




         #Tienda
         data["Tienda"].append('mercado_libre')




         #Marca: Buscar si el título contiene alguna de las marcas especificadas
         marca_encontrada = None
         for marca in marcas:
             if marca.lower() in titulo_texto.lower():
                 marca_encontrada = marca
                 break  # Si se encuentra una marca, salir del bucle
         if marca_encontrada:
             data["Marca"].append(marca_encontrada)
         else:
             data["Marca"].append("Desconocida")




     bottonSiguiente = navegador.find_element(By.CSS_SELECTOR, "a[title='Siguiente']")
     bottonSiguiente.click()




 for i in range(len(data["Marca"])):
     if data["Marca"][i] == "Moto":
         data["Marca"][i] = "Motorola"




 time.sleep(5)
 navegador.quit()




 df = pd.DataFrame(data)
 df.to_csv("database/celulares_merc2.csv", index_label="ID")




if __name__ == "__main__":
 busqueda = "celulares"
 paginas = 6
 web_scraping(busqueda, paginas)


