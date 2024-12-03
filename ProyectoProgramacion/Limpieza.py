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

def normalizar_datos(df):
   # Normalizar precios y precio sin descuento si existen
   columnas = ['Precio', 'Precio_sin_descuento']
   for columna in columnas:
       if columna in df.columns:  # Verificar si la columna existe
           df.loc[:, columna] = df[columna].replace({r'\$': '', ',': '', '"': ''}, regex=True)
           df.loc[:, columna] = pd.to_numeric(df[columna], errors='coerce')


   # Extraer solo el número de la valoración si existe
   if 'Valoracion' in df.columns:
       df['Valoracion'] = df['Valoracion'].str.extract(r'([\d.]+)').astype(float)


   #Transformar a float en caso de que no se haya aplicado
   if 'Precio' in df.columns:
       df['Precio'] = df['Precio'].astype(float)


   if 'Precio_sin_descuento' in df.columns:
       df['Precio_sin_descuento'] = df['Precio_sin_descuento'].astype(float)


   # Eliminar comillas dobles en la columna 'Titulo' si existe
   if 'Titulo' in df.columns:
       df['Titulo'] = df['Titulo'].replace({'"': ''}, regex=True)


   return df




def limpiar_datos(df):
  df = df.copy()  # Crear una copia explícita


  nulos = df.isna().mean()


  df = df.loc[:, nulos <= 0.2] #Se extraen todas las columnas que tienen mas del 20% de valores nulos


  for columna in df.select_dtypes(include=['float', 'int']): #Selecciona solo los datos de tipo numerico
      if df[columna].isna().mean() > 0:  # Si tiene nulos
          if columna == 'Precio':
              df[columna] = df[columna].fillna(df[columna].median())  #Rellenamos precio con la mediana
          else:
              df[columna] = df[columna].fillna(df[columna].mean()) #Y el resto de valores con la media


  df = df[df['Marca'].str.strip() != "Desconocida"]


  df = df.drop_duplicates().reset_index(drop=True)


  return df




def procesar_archivos(archivo_csv1, archivo_csv2):
 df1 = pd.read_csv(archivo_csv1)
 df2 = pd.read_csv(archivo_csv2)




 print("Dataframe original - Archivo 1:")
 print(df1.head())
 print("\nDataframe original - Archivo 2:")
 print(df2.head())




 # Limpiar y normalizar ambos archivos
 df1_normalizado = normalizar_datos(df1)
 df2_normalizado = normalizar_datos(df2)


 df1_limpio = limpiar_datos(df1_normalizado)
 df2_limpio = limpiar_datos(df2_normalizado)




 # Eliminar cualquier columna 'ID' antigua que no se necesite
 df1_limpio.drop(columns=['ID'], errors='ignore', inplace=True)
 df2_limpio.drop(columns=['ID'], errors='ignore', inplace=True)




 # Guardar los datos procesados sin la columna 'ID' ni el índice
 df1_limpio.to_csv("database/amazon_10.csv", index=False, sep=";", quoting=csv.QUOTE_NONE,
                        escapechar="\\")
 df2_limpio.to_csv("database/mercado_3.csv", index=False, sep=";", quoting=csv.QUOTE_NONE,
                        escapechar="\\")


 print(df1_normalizado.dtypes)
 print(df1_limpio.dtypes)


 print("\nTipo de datos - Mercado libre")


 print(df2_normalizado.dtypes)
 print(df2_limpio.dtypes)




 print("\nDataframe procesado - Archivo 1:")
 print(df1_limpio.head())
 print("\nDataframe procesado - Archivo 2:")
 print(df2_limpio.head())


 print("\nPorcentajes nulos - Amazon")
 porcentaje_nulos0 = df1.isna().mean() * 100
 print(porcentaje_nulos0)


 porcentaje_nulos3 = df1_normalizado.isna().mean() * 100
 print(porcentaje_nulos3)


 porcentaje_nulos1 = df1_limpio.isna().mean() * 100
 print(porcentaje_nulos1)


 print("\nPorcentajes nulos - Mercado libre")
 porcentaje_nulos00 = df2.isna().mean() * 100
 print(porcentaje_nulos00)


 porcentaje_nulos33 = df2_normalizado.isna().mean() * 100
 print(porcentaje_nulos33)


 porcentaje_nulos11 = df2_limpio.isna().mean() * 100
 print(porcentaje_nulos11)


 print("\nLos datos han sido limpiados, normalizados y guardados como 'celulares1_procesados.csv' y 'celulares2_procesados.csv'.")
 return df1_limpio, df2_limpio




def combinar_datos(archivo1, archivo2):
   try:
       df1 = pd.read_csv(archivo1, sep=';')
       df2 = pd.read_csv(archivo2, sep=';')


       # Concatenar los datos
       datos_concatenados = pd.concat([df1, df2], ignore_index=True)


       datos_concatenados.to_csv("database/celulares_final.csv", index=False, sep=';')


       return datos_concatenados
   except Exception as e:
       print(f"Error al combinar datos: {e}")
       return None