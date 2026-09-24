import dash
from dash import html
import dash_bootstrap_components as dbc
 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
 
app.layout = dbc.Container([
    html.P('On a desktop B shows before A, and the yellow block sits '
           'in the middle. Narrow the window and both revert.',
           className='text-muted mt-3'),
    dbc.Row([
        # A is first in the code but shows second from md upwards
        dbc.Col(html.Div('A', className='p-3 bg-primary text-white'),
                md=4, className='order-md-2'),
        dbc.Col(html.Div('B', className='p-3 bg-success text-white'),
                md=4, className='order-md-1'),
    ]),
    # Offset pushes a column to the right, leaving empty grid space
    dbc.Row([
        dbc.Col(html.Div('Centred block',
                         className='p-3 bg-warning text-center'),
                md=6, lg={'size': 4, 'offset': 4}),
    ], className='mt-3'),
], fluid=True)
 
if __name__ == '__main__':
    app.run(debug=True)
 