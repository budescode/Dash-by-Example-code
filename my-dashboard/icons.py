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
    html.H5('Bootstrap Icons', className='mt-4'),
    html.I(className='bi bi-house-fill me-2'),
    html.I(className='bi bi-table me-2'),
    html.I(className='bi bi-currency-dollar me-2'),
    html.I(className='bi bi-wifi me-2'),
    html.I(className='bi bi-gear-fill me-2'),
    html.I(className='bi bi-cloud-upload-fill me-2'),
 
    html.H5('Font Awesome', className='mt-4'),
    html.I(className='fa-solid fa-chart-line me-2'),
    html.I(className='fa-solid fa-filter me-2'),
    html.I(className='fa-solid fa-circle-check me-2'),
    html.I(className='fa-solid fa-bolt me-2'),
    html.I(className='fa-solid fa-moon me-2'),
    html.I(className='fa-brands fa-bitcoin me-2'),
])
 
if __name__ == '__main__':
    app.run(debug=True)