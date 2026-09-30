# app.py: App instance, navbar, router
import dash
from dash import html, dcc, Input, Output, callback, page_container
import dash_bootstrap_components as dbc

#populate dropdown options and filter into the shared store
from data_loader import df, REGIONS, CATEGORIES
 
app = dash.Dash(
    __name__,
    use_pages=True,
    pages_folder='pages',
    external_stylesheets=[
        dbc.themes.FLATLY,
        dbc.icons.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
    ]
)
server = app.server
 
navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand([
            html.I(className='bi bi-shop-window me-2'),
            'Sales KPI Tracker'
        ], href='/'),
        dbc.Nav([
            dbc.NavLink([html.I(className='bi bi-speedometer2 me-1'), 'Overview'],
                        href='/', active='exact'),
            dbc.NavLink([html.I(className='bi bi-bar-chart-fill me-1'), 'Categories'],
                        href='/categories', active='exact'),
            dbc.NavLink([html.I(className='bi bi-pie-chart-fill me-1'), 'Segments'],
                        href='/segments', active='exact'),
            dbc.NavLink([html.I(className='bi bi-table me-1'), 'Order Detail'],
                        href='/orders', active='exact'),
        ], navbar=True, pills=True),
    ]), color='dark', dark=True, className='mb-3'
)
 
# Shared filter bar: visible on every page, lives outside page_container
filter_bar = dbc.Card(dbc.CardBody([
    dbc.Row([
        dbc.Col([
            html.Label([html.I(className='bi bi-geo-alt-fill me-1'), 'Region'],
                       className='fw-bold'),
            dcc.Dropdown(id='region-dd', multi=True, placeholder='All regions')
        ], md=4),
        dbc.Col([
            html.Label([html.I(className='bi bi-tag-fill me-1'), 'Category'],
                       className='fw-bold'),
            dcc.Dropdown(id='cat-dd', multi=True, placeholder='All categories')
        ], md=4),
        dbc.Col([
            html.Label([html.I(className='bi bi-calendar-range me-1'), 'Date Range'],
                       className='fw-bold'),
            dcc.DatePickerRange(id='date-range', display_format='MMM DD YYYY')
        ], md=4),
    ])
]), className='mb-3 shadow-sm')
 
app.layout = dbc.Container([
    dcc.Store(id='filtered-store'),
    navbar,   # px-0 on the container lets it span the full width
    html.Div([
        filter_bar,
        page_container,   # swapped automatically based on the URL
    ], className='px-4'),   # side padding below the navbar
], fluid=True, className='px-0')


# Fill the filter controls once, when the app first loads
@callback(
    Output('region-dd', 'options'),
    Output('cat-dd',    'options'),
    Output('date-range','start_date'),
    Output('date-range','end_date'),
    Input('region-dd', 'id'),   # fires once on load
)
def init_filters(_):
    return (
        [{'label': r, 'value': r} for r in REGIONS],    # region choices
        [{'label': c, 'value': c} for c in CATEGORIES],  # categories
        df['Order Date'].min(),   # earliest date
        df['Order Date'].max(),   # latest date
    )
 
# Save the current selections; each page filters the data itself
@callback(
    Output('filtered-store', 'data'),
    Input('region-dd',  'value'),
    Input('cat-dd',     'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
)
def update_filtered_store(regions, cats, start, end):
    return {'regions': regions, 'cats': cats,
            'start': start, 'end': end}

 
if __name__ == '__main__':
    app.run(debug=True)