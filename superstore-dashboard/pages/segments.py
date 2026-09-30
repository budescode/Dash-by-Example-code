# pages/segments.py
import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from data_loader import filter_df
 
dash.register_page(__name__, path='/segments', name='Segments')
 
layout = dbc.Container([
    html.H4([
        html.I(className='bi bi-pie-chart-fill me-2'),
        'Sales by Customer Segment'
    ], className='mb-3'),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id='segment-pie'), body=True), md=6),
    ], justify='center'),   # centre the half-width column
], fluid=True)
 
@callback(
    Output('segment-pie', 'figure'),
    Input('filtered-store', 'data'),
)
def update_segments(filters):
    """Build a donut chart of sales share by customer segment."""
    dff = filter_df(filters)     # rows matching the current filters
    if dff.empty:                # the filters match no orders
        return px.pie(title='No orders match these filters')
    # total sales for each customer segment
    seg = dff.groupby('Segment')['Sales'].sum().reset_index()
    pie = px.pie(seg, values='Sales', names='Segment', hole=0.45,
                title='Sales by Segment', template='plotly_white')
    return pie