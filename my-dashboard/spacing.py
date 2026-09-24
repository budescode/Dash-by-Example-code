import dash
from dash import html
import dash_bootstrap_components as dbc
 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
 
def colour_block(label, hex_colour):
    return html.Div(
        label,
        className='p-3 text-white text-center rounded',
        style={'backgroundColor': hex_colour},
    )
 
# g-3 adds medium gutters between all columns in the row
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(colour_block('Card A', '#0D6EFD'), md=4),  # blue
        dbc.Col(colour_block('Card B', '#198754'), md=4),  # green
        dbc.Col(colour_block('Card C', '#DC3545'), md=4),  # red
    ], className='g-3'),
 
    # Common spacing scale: 0, 1, 2, 3, 4, 5 (5 = largest)
    html.Div('Padded card', className='p-3 mb-4 mt-3 border'),
    html.Div('Top margin only', className='mt-3'),
], fluid=True)
 
if __name__ == '__main__':
    app.run(debug=True)