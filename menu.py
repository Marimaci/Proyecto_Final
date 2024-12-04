import welcome as w
import dashboard1 as d1
import dashboard2 as d2
import dashboard3 as d3
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, Dash


app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH], suppress_callback_exceptions=True)


@app.callback(
   Output("page-content", "children"),
   [Input("url", "pathname")]
)
def render_page_content(pathname):
   if pathname == "/":
       return w.welcome()
   elif pathname == "/dash-1":
       return d1.dashboard()
   elif pathname == "/dash-2":
       return d2.dashboard()
   elif pathname == "/dash-3":
       return d3.dashboard()


   return html.Div(
       [
           html.H1("404: Not found", className="text-danger"),
           html.Hr(),
           html.P(f"The pathname {pathname} was not recognised..."),
       ],
       className="p-3 bg-light rounded-3",
   )


def menu_dashboard():
   SIDEBAR_STYLE = {
       "position": "fixed",
       "top": 0,
       "left": 0,
       "bottom": 0,
       "width": "16rem",
       "padding": "2rem 1rem",
       "background-color": "#f8f9fa",
   }


   CONTENT_STYLE = {
       "margin-left": "18rem",
       "margin-right": "2rem",
       "padding": "2rem 1rem",
   }


   sidebar = html.Div(
       [
           html.H2("Dashboard", className="display-6"),
           html.Hr(),
           html.P("Mercado Libre y Amazon", className="lead"),
           dbc.Nav(
               [
                   dbc.NavLink("Home", href="/", active="exact"),
                   dbc.NavLink("Dashboard 1", href="/dash-1", active="exact"),
                   dbc.NavLink("Dashboard 2", href="/dash-2", active="exact"),
                   dbc.NavLink("Dashboard 3", href="/dash-3", active="exact"),
                   dbc.NavLink("Github", href="https://github.com/Marimaci/Proyecto_Final.git", active="exact", target="_blank"),
               ],
               vertical=True,
               pills=True,
           ),
       ],
       style=SIDEBAR_STYLE,
   )


   content = html.Div(id="page-content", style=CONTENT_STYLE)


   return html.Div([dcc.Location(id="url"), sidebar, content])


app.layout = menu_dashboard()


if __name__ == "__main__":
   app.run_server(debug=True)

