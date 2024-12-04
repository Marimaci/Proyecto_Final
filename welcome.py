import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, callback, Input, Output

def welcome():
    body = html.Div(
        [
            # H# decide el tamano de letra son titulos
            html.H1("Proyecto Final"),


            # Imagenes
            html.Img(src="https://www.am.com.mx/u/fotografias/m/2024/2/14/f1280x720-558242_689917_5050.png",
                  width=300, height=200, title="Python"),

            html.Hr(),

            # P significa Parrafo
            html.H5("Objetivo: Analizar y comparar las principales características de los celulares ofrecidos en "
                    "las tiendas en línea de Amazon y Mercado Libre, enfocándose en identificar cuáles destacan más.",
                    style={"color": "#0c1a29"}),
            # Hr hace una linea de separacion
            html.Hr(),
            html.H4("Alumnos:"),
            html.Ul(
                [
                 html.Li("Delgadillo Marquez Omar Ricardo"),
                 html.Li("Felix Triche Emmanuel"),
                 html.Li("Macias Ramirez Mariana"),
                 html.Li("Otriz Vega Abril Estefania"),
                 html.Li("Romero Jeronimo Gabriel"),
                ], style={"color": "#0c1a29"}
            ),
        ]
    )
    return body
