# Proyecto_Final  :smile:
# Descripción del Problema :school:

Mercado Libre y Amazon se encuentran entre las plataformas de comercio electrónico más importantes de América Latina y del planeta, en ese orden.

En cuanto a su valoración, Amazon tiene una percepción más fuerte a nivel mundial debido a su extensa presencia internacional y su reputación en la calidad del servicio, en cambio, Mercado Libre, a pesar de ser bastante conocido en América Latina, posee una presencia más local. 

En lo que respecta a la diversidad de productos, Amazon presenta una selección más extensa gracias a su presencia mundial y sus colaboraciones con miles de vendedores; por otro lado, Mercado Libre, aunque dispone de una gran variedad de productos, se centra principalmente en el mercado de América Latina. 

En términos de precios, Mercado Libre generalmente ofrece tarifas más competitivas en la región, gracias a su enfoque local y a su modelo de costos ajustado a los mercados latinoamericanos.

Por el contrario, Amazon tiene la capacidad de vender productos a precios más altos gracias a su infraestructura global, aunque también dispone de una gran variedad de opciones con rebajas. 


# Objetivos :office:

**Preguntas a resolver**
En este análisis se compararon celulares en distintas páginas web, lo que se tomará en cuenta son precios, valoraciones y cantidades ofrecidas, también se compararán productos por marca, los productos se separarán por marca para ver cuáles son mejores, así se verá cuáles productos destacan más.

Lo que queremos saber es:

- ¿Qué marcas son mejores de acuerdo a Precio-Valoración?

- ¿Qué tienda online tiene más inventario/variedad?

- ¿Qué tiendas tienen mejores precios?

- ¿Qué marcas son más compradas?


# Recolección de Datos  :information_source:
**Mercado libre**
Se utilizó la página de mercado libre, aquí se hace la búsqueda de celulares, ya que nuestra comparación es de ello.

Los datos que se tomaron para trabajar fueron los de título, precio, valoración.
https://listado.mercadolibre.com.mx/celulares#D[A:celulares]


**Amazon** 
Se utilizó después la página de amazon, aquí se hizo el mismo procedimiento para recolectar datos que en mercado libre.

Se recolectaron exactamente los mismos atributos que en la pagina anterior
https://www.amazon.com.mx/?tag=msndeskabkmx-20&ref=pd_sl_39b6ojqq8e_e&adgrpid=1163283722832216&hvadid=72705306190847&hvnetw=o&hvqmt=e&hvbmt=be&hvdev=c&hvlocint=&hvlocphy=151132&hvtargid=kwd-72705584308339:loc-119&hydadcr=13960_10764340


# Transformación :abc:

**Diccionario de Datos
**

Tienda:

| Primary Key  |  id_tienda | INT|
| ------------ | ------------ | ------------ |
| Attribute       | nombre    | VARCHAR (255)|


Productos:

|  Primary Key | id_producto  | INT  |
| ------------ | ------------ | ------------ |
| Attribute  | título  | VARCHAR (255) |
| Attribute  |  precio |  FLOAT |
| Attribute  |  valoración | VARCHAR(255)  |
| Attribute  |  marca |  VARCHAR (100) |
|  Foreing Key | id_tienda  | INT  |


# Instrucciones de uso :clock1230:
**Indicaciones
**

Paso 1: WEB SCRAPING
Para utilizar el proyecto es correr el codigo de web scraping"Mercado_Libre.py" y "Amazon.py".

Paso 2: LIMPIEZA DE DATOS
En esta ocacion corre el codigo "limpieza_datos.py" para limpiar los datos extraidos de web scraping, de esta manera se podra trabajar de forma correcta los datos obtenidos.

Paso 3: CREAR BASE DE DATOS
Se creo una base de datos en MySQL donde se guardaran todos los datos ya procesados, aqui es donde se tiene que poner el query "script_sql.sql" en MySQL.

Paso 4: MIGRACION DE DATOS
Se tiene que correr el codigo de "migracion_a_bd.py" en python, esto con el fin de pasar los datos procesados a sql.

Paso 5: CREACION DE DASHBOARD
- El dashboar uno es de amazon, el segundo de mercado libre y el tercero de comparación de ambas.
- El welcome solo es la bienvenida a la pagina.
- El menú es donde se llama a todos los dashboards y el welcome para tenerlo dentro de un mismo lugar.

# Colaboradores :beginner:
Delgadillo Marquez Omar Ricardo

Felix Triche Emmanuel

Macias Ramirez Mariana

Ortiz Vega Abril Estefania

Romero Jeronimo Gabriel

