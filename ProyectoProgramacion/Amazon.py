import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px


# Leer los datos
df = pd.read_csv("database/celulares_final.csv", sep=";")


# Filtrar solo Amazon
amazon_data = df[df["Tienda"] == "amazon"]


# Crear la app Dash
app = dash.Dash(__name__)


# Definir los intervalos de precios
bins = [1000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 55000]
labels = ["1000-5000", "5000-10000", "10000-15000", "15000-20000", "20000-25000", "25000-30000", "30000-35000",
         "35000-40000", "40000-45000", "45000-55000"]


# Layout del dashboard
app.layout = html.Div([
   html.H1("Dashboard de Celulares en Amazon", style={"text-align": "center"}),


   # Segunda gráfica: Cantidad de Celulares por Marca
   html.Div([
       html.H2("Cantidad de Celulares por Marca"),
       dcc.Graph(
           id="cantidad-marca",
           figure=px.bar(
               amazon_data.groupby("Marca").size().reset_index(name="Cantidad"),
               x="Marca",
               y="Cantidad",
               title="Cantidad de Celulares por Marca en Amazon",
               labels={"Cantidad": "Número de Modelos"},
               color="Marca"
           )
       )
   ]),


   # Nueva gráfica: Distribución de Celulares por Intervalo de Precios
   html.Div([
       html.H2("Distribución de Celulares por Intervalo de Precios"),
       dcc.Dropdown(
           id="marca-dropdown",
           options=[{"label": marca, "value": marca} for marca in amazon_data["Marca"].unique()],
           value=amazon_data["Marca"].unique()[0],  # Marca inicial seleccionada
           clearable=False
       ),
       dcc.Graph(id="rangos-precios-pie")
   ]),


   # Tercera gráfica: Dispersión de Valoraciones vs. Precio
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




# Callback para actualizar la gráfica de distribución por intervalos de precios
@app.callback(
   Output("rangos-precios-pie", "figure"),
   Input("marca-dropdown", "value")
)
def update_rangos_precios_pie(selected_marca):
   # Filtrar los datos según la marca seleccionada
   filtered_data = amazon_data[amazon_data["Marca"] == selected_marca]


   # Crear los intervalos de precios
   filtered_data['Rango de Precio'] = pd.cut(filtered_data["Precio"], bins=bins, labels=labels, right=False)


   # Contar la cantidad de celulares por intervalo de precio
   rangos_precios_count = filtered_data.groupby("Rango de Precio").size().reset_index(name="Cantidad")


   # Crear la gráfica de pie
   fig = px.pie(
       rangos_precios_count,
       names="Rango de Precio",
       values="Cantidad",
       title=f"Distribución de Celulares por Intervalo de Precios para {selected_marca}",
       labels={"Cantidad": "Número de Celulares"}
   )


   return fig




# Callback para actualizar la gráfica de dispersión
@app.callback(
   Output("dispersión-valoraciones-precio", "figure"),
   Input("marca-dispersion-dropdown", "value")
)
def update_dispersion(selected_marca):
   if selected_marca == "Todas":
       filtered_data = amazon_data
       title = "Relación entre Precio y Valoraciones por Marca"
   else:
       filtered_data = amazon_data[amazon_data["Marca"] == selected_marca]
       title = f"Relación entre Precio y Valoraciones para {selected_marca}"


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




# Ejecutar la app
if __name__ == "__main__":
   app.run_server(debug=True)