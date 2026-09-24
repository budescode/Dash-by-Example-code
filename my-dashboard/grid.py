import dash
from dash import html
import dash_bootstrap_components as dbc
 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
 
app.layout = dbc.Container([
    html.P('Resize the browser window: on a narrow screen the sidebar '
           'stacks above the main content.',
           className='text-muted mt-3'),
    dbc.Row([
        # Any split works as long as the two md values add up to 12.
        # The second row below shows 4 and 8.
        dbc.Col(
            html.Div('Sidebar', className='p-3 bg-primary text-white'),
            md=3    # 3 of the 12 units: a quarter of the row
        ),
        dbc.Col(
            html.Div('Main Content', className='p-3 bg-light border'),
            md=9    # the other 9 units
        ),
    ]),
    dbc.Row([
        dbc.Col(html.Div('md=4', className='p-3 bg-success text-white'),
                md=4),
        dbc.Col(html.Div('md=8', className='p-3 bg-light border'),
                md=8),
    ], className='mt-3'),
], fluid=True)
 
if __name__ == '__main__':
    app.run(debug=True)
 