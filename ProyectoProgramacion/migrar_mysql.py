import pandas as pd
import mysql.connector


def insertar_datos():

   # Conexión a MySQL
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="celulares",
        port=3307
    )
    cursor = conexion.cursor()


   # Leer CSV
    df = pd.read_csv("database/celulares_final.csv", delimiter=";")


   # Insertar tiendas (si es necesario)
    tiendas = df['Tienda'].unique()
    for tienda in tiendas:
       # Verificar si la tienda ya existe
        cursor.execute("SELECT id_tienda FROM tiendas WHERE nombre = %s", (tienda,))
        resultado = cursor.fetchall()


        if not resultado:  # Si la tienda no existe
            cursor.execute("INSERT INTO tiendas (nombre) VALUES (%s)", (tienda,))


   # Obtener IDs de tiendas
    cursor.execute("SELECT id_tienda, nombre FROM tiendas")
    id_tienda = {nombre: id for id, nombre in cursor.fetchall()}


    for row in df.itertuples(index=False):
       # Verificar si el producto ya existe
        cursor.execute("SELECT titulo FROM productos WHERE titulo = %s", (row.Titulo,))
        productos = cursor.fetchall()


        if not productos:  # Si el producto no existe
            cursor.execute("""
                    INSERT INTO productos (titulo, precio, valoracion, marca, id_tienda)
                    VALUES (%s, %s, %s, %s, %s)
                """, (row.Titulo, row.Precio, row.Valoracion, row.Marca, id_tienda[row.Tienda]))




   # Guardar cambios
    conexion.commit()
    cursor.close()
    conexion.close()




if __name__ == "__main__":
    insertar_datos()
