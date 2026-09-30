"""Top 10 states by revenue."""
import dash
from dash import html, dcc
import plotly.express as px
import dash_bootstrap_components as dbc
from data_loader import df
 
dash.register_page(__name__, path='/revenue', name='Revenue')
 
# Which states drive revenue. Sum payment per
# state, then take the ten biggest for the bar.
by_state = df.groupby('customer_state',
                      as_index=False)['payment_value'].sum()
top = by_state.sort_values('payment_value',
                           ascending=False).head(10)
 
revenue_fig = px.bar(
    top, x='payment_value', y='customer_state',
    orientation='h', title='Top 10 States by Revenue',
    labels={'payment_value': 'Revenue (R$)', 'customer_state': 'State'},
    template='plotly_white',
    color_discrete_sequence=['#00B4D8'])
revenue_fig.update_layout(
    yaxis={'categoryorder': 'total ascending'})
revenue_fig.update_xaxes(tickprefix='R$', tickformat=',.0f')
 
layout = dbc.Container([
    html.H4([html.I(className='fa-solid fa-map-location-dot me-2'),
             'Revenue by State']),
    html.P("Total revenue by customer state, top ten only. "
           "Sales are concentrated: one state brings in more "
           "than the next few combined, with the southeast "
           "dominating.",
           className='text-muted'),
    dcc.Graph(figure=revenue_fig),
])