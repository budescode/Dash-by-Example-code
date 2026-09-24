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
    html.H5('Sizes: fs-1 (largest) to fs-6 (smallest)',
            className='mt-4'),
    html.I(className='bi bi-bar-chart-fill fs-1 me-2'),
    html.I(className='bi bi-bar-chart-fill fs-2 me-2'),
    html.I(className='bi bi-bar-chart-fill fs-3 me-2'),
    html.I(className='bi bi-bar-chart-fill fs-4 me-2'),
    html.I(className='bi bi-bar-chart-fill fs-5 me-2'),
    html.I(className='bi bi-bar-chart-fill fs-6 me-2'),
 
    html.H5('Theme colours', className='mt-4'),
    html.I(className='bi bi-circle-fill fs-3 me-2 text-primary'),
    html.I(className='bi bi-circle-fill fs-3 me-2 text-secondary'),
    html.I(className='bi bi-circle-fill fs-3 me-2 text-success'),
    html.I(className='bi bi-circle-fill fs-3 me-2 text-danger'),
    html.I(className='bi bi-circle-fill fs-3 me-2 text-warning'),
    html.I(className='bi bi-circle-fill fs-3 me-2 text-info'),
    html.I(className='bi bi-circle-fill fs-3 me-2 text-muted'),
 
    html.H5('Custom colour with style', className='mt-4'),
    html.I(className='bi bi-circle-fill fs-3 me-2',
           style={'color': '#00B4D8'}),
    html.I(className='fa-solid fa-fire fs-3 me-2',
           style={'color': 'red'}),
])
 
if __name__ == '__main__':
    app.run(debug=True)