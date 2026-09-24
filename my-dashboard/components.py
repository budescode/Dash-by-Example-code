import dash
from dash import html
import dash_bootstrap_components as dbc
 
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY,
        dbc.icons.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
    ],
    suppress_callback_exceptions=True
)
 
app.layout = dbc.Container([
 
    html.H5('Buttons', className='mt-4'),
    dbc.Button('Primary', color='primary', className='me-2'),
    dbc.Button('Success', color='success', className='me-2'),
    dbc.Button('Danger',  color='danger',  className='me-2'),
    dbc.Button([html.I(className='bi bi-download me-2'), 'With icon'],
               color='secondary', outline=True),
 
    html.H5('Text input', className='mt-4'),
    dbc.Input(id='search', placeholder='Type to search...',
              type='text'),
 
    html.H5('Select', className='mt-4'),
    dbc.Select(
        id='region',
        options=[{'label': 'North', 'value': 'north'},
                 {'label': 'South', 'value': 'south'}],
        value='north',
    ),
 
    html.H5('Card', className='mt-4'),
    dbc.Card(
        dbc.CardBody([
            html.H6('Total Revenue', className='text-muted'),
            html.H3('$24,500'),
        ]),
        className='shadow-sm',
    ),
 
    html.H5('Alert and Badge', className='mt-4'),
    dbc.Alert('Saved successfully.', color='success'),
    html.Span(['Orders ', dbc.Badge('24', color='primary')]),
 
], className='mb-5')
 
if __name__ == '__main__':
    app.run(debug=True)