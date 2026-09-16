import dash
from dash import html
import dash_bootstrap_components as dbc
 
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY,
        dbc.icons.BOOTSTRAP,       # Bootstrap Icons
        dbc.icons.FONT_AWESOME,    # Font Awesome Free
    ],
    suppress_callback_exceptions=True
)
 
app.layout = dbc.Container([
    html.H1([
        html.I(className='bi bi-speedometer2 me-2 text-primary'),
        'Dash is working!'
    ], className='text-center mt-4'),
    dbc.Alert([
        html.I(className='fa-solid fa-circle-check me-2'),
        'Both icon libraries loaded successfully!'
    ], color='success', className='d-flex align-items-center mt-3')
])
 
if __name__ == '__main__':
    app.run(debug=True)