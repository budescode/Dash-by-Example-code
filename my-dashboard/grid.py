import dash
from dash import html
import dash_bootstrap_components as dbc
 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
 
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div('Sidebar', className='p-3 bg-primary text-white'),
            md=3
        ),
        dbc.Col(
            html.Div('Main Content', className='p-3 bg-light border'),
            md=9
        ),
    ]),
], fluid=True)
 
if __name__ == '__main__':
    app.run(debug=True)