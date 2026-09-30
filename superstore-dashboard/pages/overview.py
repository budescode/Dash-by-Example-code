# pages/overview.py
import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from data_loader import filter_df
 
dash.register_page(__name__, path='/', name='Overview')
 
KPI_COLOR = '#2C3E50'   # one accent colour for every KPI card
 
def kpi_card(title, value, subtitle, color, icon_class):
    """Build one KPI card: icon, uppercase label, value, and subtitle,
    with a coloured left border. Used for all four cards."""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className=f'{icon_class} fs-4', style={'color': color}),
            ], className='mb-2'),
            html.P(title, className='text-muted mb-1',
                   style={'fontSize':'0.75rem','textTransform':'uppercase',
                          'letterSpacing':'0.08em'}),
            html.H3(value, className='fw-bold mb-0', style={'color': color}),
            html.P(subtitle, className='text-muted mt-1 mb-0',
                   style={'fontSize':'0.8rem'}),
        ])
    ], className='shadow-sm h-100',
       style={'borderLeft': f'5px solid {color}', 'borderRadius':'8px'})
 
layout = dbc.Container([
    dbc.Row(id='kpi-row', className='mb-3 g-3'),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id='trend-chart'), body=True), md=6),
        dbc.Col(dbc.Card(dcc.Graph(id='top-states'), body=True), md=6),
    ], className='mb-3'),
], fluid=True)
 
@callback(
    Output('kpi-row',     'children'),
    Output('trend-chart', 'figure'),
    Output('top-states',  'figure'),
    Input('filtered-store', 'data'),
)
def update_overview(filters):
    """Rebuild the KPI cards, the trend line, and the top-states bar
    from the filtered data. Runs whenever the filters change."""
    dff = filter_df(filters)      # rows matching the current filters
    if dff.empty:                 # the filters match no orders
        empty = px.line(title='No orders match these filters')
        return [], empty, empty
 
    # the four headline numbers
    revenue = dff['Sales'].sum()
    orders  = dff['Order ID'].nunique()   # distinct orders
    aov     = revenue / orders if orders else 0
    profit  = dff['Profit'].sum()
 
    kpi_row = dbc.Row([
        dbc.Col(kpi_card('Total Revenue',   f'${revenue:,.0f}', 'All orders',
                        KPI_COLOR, 'bi bi-currency-dollar'), md=3),
        dbc.Col(kpi_card('Total Orders',    f'{orders:,}', 'Unique orders',
                        KPI_COLOR, 'bi bi-bag-check-fill'), md=3),
        dbc.Col(kpi_card('Avg Order Value', f'${aov:,.0f}', 'Per order',
                        KPI_COLOR, 'bi bi-calculator-fill'), md=3),
        dbc.Col(kpi_card('Total Profit',    f'${profit:,.0f}', 'Net profit',
                        KPI_COLOR, 'fa-solid fa-sack-dollar'), md=3),
    ], className='g-3')
 
    # monthly sales, split by segment, for the trend line
    monthly = dff.groupby(['Month','Segment']).agg(
        Sales=('Sales', 'sum'),
    ).reset_index()
    trend = px.line(monthly, x='Month', y='Sales', color='Segment',
                    title='Monthly Sales by Segment', markers=True,
                    template='plotly_white')
    trend.update_layout(margin=dict(t=50,b=20,l=20,r=20), hovermode='x unified')
 
 
    # the ten states with the highest total sales
    by_state = dff.groupby('State', as_index=False)['Sales'].sum()
    top = by_state.sort_values('Sales', ascending=False).head(10)
    top_states = px.bar(top, x='Sales', y='State', orientation='h',
                        title='Top 10 States by Sales', template='plotly_white')
    top_states.update_layout(margin=dict(t=50, b=20, l=20, r=20),
                             yaxis={'categoryorder': 'total ascending'})
    return kpi_row, trend, top_states