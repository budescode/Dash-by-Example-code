# pages/categories.py
import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from data_loader import filter_df
 
dash.register_page(__name__, path='/categories', name='Categories')
 
layout = dbc.Container([
    html.H4([
        html.I(className='bi bi-bar-chart-fill me-2'),
        'Sales by Category'
    ], className='mb-3'),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id='cat-bar'), body=True), md=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id='discount-scatter'), body=True),
                md=12),
    ], className='mt-3'),
], fluid=True)
 
@callback(
    Output('cat-bar', 'figure'),
    Output('discount-scatter', 'figure'),
    Input('filtered-store', 'data'),
)
def update_categories(filters):
    """Build the two category charts from the filtered data:
    the sub-category sales bar and the discount-vs-profit view."""
    dff = filter_df(filters)     # rows matching the current filters
    if dff.empty:                # the filters match no orders
        empty = px.bar(title='No orders match these filters')
        return empty, empty
    # sales per sub-category, coloured by category
    cat = dff.groupby(['Category','Sub-Category'])['Sales'].sum().reset_index()
    bar = px.bar(cat, x='Sub-Category', y='Sales', color='Category',
                title='Sales by Sub-Category', template='plotly_white',
                text_auto='.2s')
    bar.update_layout(margin=dict(t=50,b=80,l=20,r=20))
 
    # per sub-category: total sales, total profit, avg discount
    prof = dff.groupby('Sub-Category').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Discount=('Discount', 'mean'),
    ).reset_index()
    # tag each sub-category as Profit or Loss
    prof['Result'] = prof['Profit'].apply(lambda p: 'Profit' if p >= 0 else 'Loss')
    # one bubble per sub-category: discount (x) vs profit (y)
    scatter = px.scatter(
        prof, x='Discount', y='Profit',
        size='Sales', color='Result', hover_name='Sub-Category',
        color_discrete_map={'Profit': '#28a745', 'Loss': '#dc3545'},
        title='Discount vs Profit by Sub-Category',
        template='plotly_white', size_max=40)
    # break-even line at profit = 0
    scatter.add_hline(y=0, line_dash='dash', line_color='gray')
    scatter.update_layout(margin=dict(t=50, b=40, l=20, r=20))
    return bar, scatter