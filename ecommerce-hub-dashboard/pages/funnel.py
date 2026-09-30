"""Order fulfilment funnel (home, route '/')."""
import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from data_loader import df
 
dash.register_page(__name__, path='/', name='Funnel')
 
# Each step of the order journey, from placed to delivered.
status_order = ['created', 'approved', 'processing',
                'shipped', 'delivered']
funnel_data = []
for status in status_order:
    reached = status_order[status_order.index(status):]
    orders_at = df[df['order_status'].isin(reached)]
    funnel_data.append({
        'stage': status.title(),
        'orders': orders_at['order_id'].nunique(),
    })
 
funnel_fig = px.funnel(
    pd.DataFrame(funnel_data), x='orders', y='stage',
    labels={'orders': 'Orders', 'stage': 'Stage'},
    title='Order Fulfilment Funnel', template='plotly_white',
    color_discrete_sequence=['#00B4D8'])
 
layout = dbc.Container([
    html.H4([html.I(className='fa-solid fa-filter me-2'),
             'Customer Funnel']),
    html.P("Each step of the order journey, from placed to "
           "delivered.",
           className='text-muted'),
    dcc.Graph(figure=funnel_fig),
])
 