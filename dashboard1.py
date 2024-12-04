import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, callback, Input, Output


# Leer los datos
df = pd.read_csv("database/celulares_final.csv", sep=";")


# Filtrar solo Amazon
amazon_data = df[df["Tienda"] == "amazon"]


# Definir los intervalos de precios
bins = [1000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 55000]
labels = [
   "1000-5000", "5000-10000", "10000-15000", "15000-20000", "20000-25000",
   "25000-30000", "30000-35000", "35000-40000", "40000-45000", "45000-55000"
]


# Función para crear la gráfica de barras
def grafica_barras():
   grouped_data = amazon_data.groupby("Marca").size().reset_index(name="Cantidad")
   fig = px.bar(
       grouped_data,
       x="Marca",
       y="Cantidad",
       title="Cantidad de Celulares por Marca en Amazon",
       labels={"Cantidad": "Número de Modelos"},
       color="Marca"
   )
   return fig


# Función para crear la gráfica de pie
def grafica_pie(marca):
   filtered_data = amazon_data[amazon_data["Marca"] == marca]
   filtered_data['Rango de Precio'] = pd.cut(filtered_data["Precio"], bins=bins, labels=labels, right=False)
   rangos_precios_count = filtered_data.groupby("Rango de Precio").size().reset_index(name="Cantidad")
   fig = px.pie(
       rangos_precios_count,
       names="Rango de Precio",
       values="Cantidad",
       title=f"Distribución de Celulares por Intervalo de Precios para {marca}",
       labels={"Cantidad": "Número de Celulares"}
   )
   return fig


# Función para crear la gráfica de dispersión
def grafica_dispersion(marca):
   if marca == "Todas":
       filtered_data = amazon_data
       title = "Relación entre Precio y Valoraciones por Marca"
   else:
       filtered_data = amazon_data[amazon_data["Marca"] == marca]
       title = f"Relación entre Precio y Valoraciones para {marca}"
   fig = px.scatter(
       filtered_data,
       x="Precio",
       y="Valoracion",
       color="Marca",
       title=title,
       labels={"Precio": "Precio (MXN)", "Valoracion": "Valoración"},
       hover_data=["Titulo"]
   )
   return fig


# Definir el layout
def dashboard():
   body = html.Div([
       html.H1("Dashboard de Celulares en Amazon", style={"text-align": "center"}),
       html.Div([
           html.H2("Cantidad de Celulares por Marca"),
           dcc.Graph(id="cantidad-marca", figure=grafica_barras())
       ]),
       html.Div([
           html.H2("Distribución de Celulares por Intervalo de Precios"),
           dcc.Dropdown(
               id="marca-dropdown",
               options=[{"label": marca, "value": marca} for marca in amazon_data["Marca"].unique()],
               value=amazon_data["Marca"].unique()[0],
               clearable=False
           ),
           dcc.Graph(id="rangos-precios-pie")
       ]),
       html.Div([
           html.H2("Dispersión de Valoraciones vs. Precio"),
           dcc.Dropdown(
               id="marca-dispersion-dropdown",
               options=[{"label": "Todas las Marcas", "value": "Todas"}] +
                       [{"label": marca, "value": marca} for marca in amazon_data["Marca"].unique()],
               value="Todas",
               clearable=False
           ),
           dcc.Graph(id="dispersión-valoraciones-precio")
       ])
   ])
   return body


# Crear la app Dash
app = dash.Dash(__name__)
app.layout = dashboard()


# Callbacks para actualizar las gráficas
@callback(
   Output("rangos-precios-pie", "figure"),
   Input("marca-dropdown", "value")
)
def update_rangos_precios_pie(selected_marca):
   return grafica_pie(selected_marca)


@callback(
   Output("dispersión-valoraciones-precio", "figure"),
   Input("marca-dispersion-dropdown", "value")
)
def update_dispersion(selected_marca):
   return grafica_dispersion(selected_marca)


# Ejecutar la app
if __name__ == "__main__":
   app.run_server(debug=True)

