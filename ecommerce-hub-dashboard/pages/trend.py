"""Monthly order volume as a line chart."""
import dash
from dash import html, dcc
import plotly.express as px
import dash_bootstrap_components as dbc
from data_loader import df
 
dash.register_page(__name__, path='/trend', name='Trend')
 
# Monthly order volume. A count of the distinct
# orders placed in each month, across the whole dataset.
monthly = (df.groupby('month')['order_id']
           .nunique().reset_index(name='orders'))
 
trend_fig = px.line(
    monthly, x='month', y='orders', markers=True,
    labels={'month': 'Month', 'orders': 'Orders'},
    title='Monthly Order Volume', template='plotly_white',
    color_discrete_sequence=['#00B4D8'])
 
layout = dbc.Container([
    html.H4([html.I(className='fa-solid fa-chart-line me-2'),
             'Monthly Orders']),
    html.P("Order volume per month, counting distinct "
           "orders. It reveals growth, seasonal peaks, and "
           "quiet stretches over time.",
           className='text-muted'),
    dcc.Graph(figure=trend_fig),
])