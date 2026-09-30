"""E-commerce hub: multi-page shell with a top navbar."""
import dash
from dash import html
import dash_bootstrap_components as dbc
 
# use_pages=True turns on Dash's page registry: every file
# in pages/ that calls register_page() becomes a route.
app = dash.Dash(
    __name__, use_pages=True,
    external_stylesheets=[
        dbc.themes.FLATLY,
        dbc.icons.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
    ],
)
 
# One navbar link per page, each with a Font Awesome icon.
navbar = dbc.NavbarSimple(
    brand='E-Commerce Analytics Hub',
    color='primary', dark=True, fluid=True, className='mb-4',
    children=[
        dbc.NavLink(
            [html.I(className='fa-solid fa-filter me-1'),
             'Funnel'], href='/'),
        dbc.NavLink(
            [html.I(className='fa-solid fa-chart-line me-1'),
             'Trend'], href='/trend'),
        dbc.NavLink(
            [html.I(className='fa-solid fa-map-location-dot me-1'),
             'Revenue'], href='/revenue'),
        dbc.NavLink(
            [html.I(className='bi bi-table me-1'),
             'Orders'], href='/orders'),
    ],
)
 
# page_container renders whichever page matches the URL.
app.layout = dbc.Container(
    [navbar, dash.page_container], fluid=True, className='px-0')
 
if __name__ == '__main__':
    app.run(debug=True)