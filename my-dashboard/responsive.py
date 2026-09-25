import dash
from dash import html
import dash_bootstrap_components as dbc
 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY,
                                                dbc.icons.BOOTSTRAP])
 
sidebar_content = html.Div([
    html.H5('Filters', className='mb-3'),
    dbc.Nav([
        dbc.NavLink('Region',   href='#', active=True),
        dbc.NavLink('Category', href='#'),
    ], vertical=True, pills=True),
], className='p-3 bg-light border-end h-100')
 
mobile_menu = dbc.Button(
    html.I(className='bi bi-list fs-3'),
    color='light', className='m-2',
)
 
app.layout = html.Div([
    html.P('Resize the browser window: the Filters panel shows on a '
           'desktop, and a menu button takes its place on a phone.',
           className='text-muted m-3'),
    # Hidden on screens smaller than md (e.g. collapse a sidebar on mobile)
    html.Div(sidebar_content, className='d-none d-md-block'),
 
    # Only visible on small screens (e.g. a mobile-only hamburger menu)
    html.Div(mobile_menu, className='d-block d-md-none'),
])
 
if __name__ == '__main__':
    app.run(debug=True)