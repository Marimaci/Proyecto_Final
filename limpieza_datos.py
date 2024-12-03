
import csv
import pandas as pd


def normalizar_datos(df):
    columnas = ['Precio', 'Precio_sin_descuento']
    for columna in columnas:
        if columna in df.columns:  # Verificamos si la columna existe
            df.loc[:, columna] = df[columna].replace({r'\$': '', ',': '', '"': ''}, regex=True) #Remplazamos los valores $, '' y " usando replace
            df.loc[:, columna] = pd.to_numeric(df[columna], errors='coerce')

    #Verificamos si la valoracion existe
    if 'Valoracion' in df.columns:
        df['Valoracion'] = df['Valoracion'].str.extract(r'([\d.]+)').astype(float)
        #Fuente: https://pandas.pydata.org/docs/reference/api/pandas.Series.str.extract.html

    #Transformamos todos los valores numerico en float.
    if 'Precio' in df.columns:
        df['Precio'] = df['Precio'].astype(float)

    if 'Precio_sin_descuento' in df.columns:
        df['Precio_sin_descuento'] = df['Precio_sin_descuento'].astype(float)


    return df


def limpiar_datos(df):
   df = df.copy()

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

    df1_normalizado = normalizar_datos(df1)
    df2_normalizado = normalizar_datos(df2)

    df1_limpio = limpiar_datos(df1_normalizado)
    df2_limpio = limpiar_datos(df2_normalizado)

    #Condicion para que se extraigan los datos de precio y precio sin descuento que sean menores a 1000
    if 'Precio' in df1_limpio.columns:
        df1_limpio = df1_limpio[df1_limpio['Precio'] >= 1000]
    if 'Precio_sin_descuento' in df1_limpio.columns:
        df1_limpio = df1_limpio[df1_limpio['Precio_sin_descuento'] >= 1000]

    if 'Precio' in df2_limpio.columns:
        df2_limpio = df2_limpio[df2_limpio['Precio'] >= 1000]
    if 'Precio_sin_descuento' in df2_limpio.columns:
        df2_limpio = df2_limpio[df2_limpio['Precio_sin_descuento'] >= 1000]


    df1_limpio.drop(columns=['ID'], errors='ignore', inplace=True)
    df2_limpio.drop(columns=['ID'], errors='ignore', inplace=True)

    #Referencia: https://docs.python.org/3/library/csv.html
    #QUOTE_NONE sirve para que ningun valor quede con comillas
    df1_limpio.to_csv("database/amazon_10.csv", index=False, sep=";", quoting=csv.QUOTE_NONE)
    df2_limpio.to_csv("database/mercado_3.csv", index=False, sep=";", quoting=csv.QUOTE_NONE)

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




if __name__ == "__main__":
  archivo1 = "database/celulares_amazon2.csv"
  archivo2 = "database/celulares_merc2.csv"

  procesar_archivos(archivo1, archivo2)

  combinar_datos("database/amazon_10.csv", "database/mercado_3.csv")
