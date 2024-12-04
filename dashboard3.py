import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, callback, Input, Output




# Leer los datos
df = pd.read_csv("database/celulares_final.csv", sep=";")




# Filtrar datos por tienda
amazon_data = df[df["Tienda"] == "amazon"]
mercado_libre_data = df[df["Tienda"] == "mercado_libre"]




# Definir los intervalos de precios
bins = [1000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 55000, 65000]
labels = [
  "1000-5000", "5000-10000", "10000-15000", "15000-20000", "20000-25000",
  "25000-30000", "30000-35000", "35000-40000", "40000-45000", "45000-55000", "55000-65000"
]




# Función para crear la gráfica de caja
def grafica_caja():
  fig = px.box(
      df,
      x="Marca",
      y="Valoracion",
      color="Marca",
      title="Distribución de Valoraciones por Marca",
      labels={"Valoracion": "Valoración", "Marca": "Marca"},
      color_discrete_sequence=px.colors.sequential.Darkmint_r
  )
  fig.update_traces(marker=dict(opacity=0.8))
  fig.update_layout(
      font=dict(size=16),
      plot_bgcolor="#566c7d",
      paper_bgcolor="#aec2cf",
      font_color="#0a1c27"
  )


  return fig




# Función para crear la gráfica de barras comparativa
def grafica_barras_comparativa():
  grouped_data = df.groupby(["Tienda", "Marca"]).size().reset_index(name="Cantidad")
  fig = px.bar(
      grouped_data,
      x="Marca",
      y="Cantidad",
      color="Tienda",
      title="Cantidad de Celulares por Marca (Amazon vs Mercado Libre)",
      labels={"Cantidad": "Número de Modelos"},
      color_discrete_sequence=px.colors.sequential.Darkmint
  )
  fig.update_traces(marker=dict(opacity=0.7))
  fig.update_layout(
      font=dict(size=16),
      plot_bgcolor="#566c7d",
      paper_bgcolor="#aec2cf",
      font_color="#0a1c27"
  )
  return fig




# Función para crear la gráfica de intervalos de precios comparativa
def grafica_lineas_precios(marca):
  filtered_data = df[df["Marca"] == marca]
  filtered_data['Rango de Precio'] = pd.cut(filtered_data["Precio"], bins=bins, labels=labels, right=True)
  rangos_precios_count = filtered_data.groupby(["Rango de Precio", "Tienda"]).size().reset_index(name="Cantidad")
  fig = px.line(
      rangos_precios_count,
      x="Rango de Precio",
      y="Cantidad",
      color="Tienda",
      markers=True,
      title=f"Distribución de Celulares por Intervalo de Precios para {marca}",
      labels={"Cantidad": "Número de Celulares", "Rango de Precio": "Intervalo de Precios"},
      color_discrete_sequence=px.colors.sequential.Greens_r
  )
  fig.update_layout(
      font=dict(size=16),
      plot_bgcolor="#566c7d",
      paper_bgcolor="#aec2cf",
      font_color="#0a1c27"
  )


  return fig




# Función para crear la gráfica de dispersión
def grafica_dispersion_comparativa(marca):
  if marca == "Todas":
      filtered_data = df
      title = "Relación entre Precio y Valoraciones (Amazon vs Mercado Libre)"
  else:
      filtered_data = df[df["Marca"] == marca]
      title = f"Relación entre Precio y Valoraciones para {marca} (Amazon vs Mercado Libre)"
  fig = px.scatter(
      filtered_data,
      x="Precio",
      y="Valoracion",
      color="Tienda",
      title=title,
      labels={"Precio": "Precio (MXN)", "Valoracion": "Valoración"},
      color_discrete_sequence=px.colors.sequential.Blues_r,
      hover_data=["Titulo"]
  )
  fig.update_traces(marker=dict(size=10, opacity=0.9))
  fig.update_layout(
      plot_bgcolor="#566c7d",
      paper_bgcolor="#aec2cf",
      font_color="#0a1c27"
  )


  return fig




# Definir el layout
def dashboard():
  return html.Div([
      html.H1("Dashboard Comparativo de Celulares: Amazon vs Mercado Libre", style={"text-align": "center"}),




      # Gráfica de caja
      html.Div([
          dcc.Graph(id="grafico-caja", figure=grafica_caja()),
          dcc.Graph(id="cantidad-marca-comparativa", figure=grafica_barras_comparativa()),


          html.H2("Distribución de Celulares por Intervalo de Precios", style={"backgroundColor": "#aec2cf",
                                                                               "color": "#0c1a29"}),
          dcc.Dropdown(
              id="marca-dropdown-comparativa",
              options=[{"label": marca, "value": marca} for marca in df["Marca"].unique()],
              value=df["Marca"].unique()[0],
              clearable=False
          ),
          dcc.Graph(id="rangos-precios-comparativa")
      ], style={"backgroundColor": "#aec2cf", "padding": "20px"}),


      html.Div([
          html.H2("Dispersión de Valoraciones vs. Precio", style={"backgroundColor": "#aec2cf",
                                                                  "color": "#0c1a29"}),
          dcc.Dropdown(
              id="marca-dispersion-dropdown-comparativa",
              options=[{"label": "Todas las Marcas", "value": "Todas"}] +
                      [{"label": marca, "value": marca} for marca in df["Marca"].unique()],
              value="Todas",
              clearable=False
          ),
          dcc.Graph(id="dispersión-valoraciones-precio-comparativa")
      ], style={"backgroundColor": "#aec2cf", "padding": "20px"})
  ])




# Crear la app Dash
app = dash.Dash(__name__)
app.layout = dashboard()




# Callbacks para actualizar las gráficas
@callback(
  Output("rangos-precios-comparativa", "figure"),
  Input("marca-dropdown-comparativa", "value")
)
def update_rangos_precios_comparativa(selected_marca):
  return grafica_lineas_precios(selected_marca)




@callback(
  Output("dispersión-valoraciones-precio-comparativa", "figure"),
  Input("marca-dispersion-dropdown-comparativa", "value")
)
def update_dispersion_comparativa(selected_marca):
  return grafica_dispersion_comparativa(selected_marca)




# Ejecutar la app
if __name__ == "__main__":
  app.run_server(debug=True)