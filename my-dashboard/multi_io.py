import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
 
df = pd.DataFrame({
    'Region':     ['North']*4 + ['South']*4,
    'Category':   ['Furniture', 'Tech'] * 4,
    'Order Date': pd.to_datetime(
        ['2024-01-15', '2024-02-20', '2024-03-10', '2024-04-05'] * 2),
    'Sales':      [1200, 1800, 900, 1500, 1100, 1700, 800, 1400],
    'Profit':     [200, 400, 150, 300, 180, 380, 120, 260],
})
 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
 
app.layout = dbc.Container([
    html.P('Pick a region or a date range and watch the KPI and '
           'both charts update together.', className='text-muted mt-3'),
    dcc.Dropdown(id='region-filter',
                 options=[{'label': r, 'value': r}
                          for r in df['Region'].unique()],
                 value='North', clearable=False),
    dcc.DatePickerRange(id='date-range',
                        start_date=df['Order Date'].min(),
                        end_date=df['Order Date'].max()),
    html.H3(id='kpi-revenue', className='mt-3'),
    dcc.Graph(id='sales-chart'),
    dcc.Graph(id='profit-chart'),
])
 
@callback(
    Output('sales-chart', 'figure'),
    Output('profit-chart', 'figure'),
    Output('kpi-revenue', 'children'),
    Input('region-filter', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
)
def update_all(region, start, end):
    dff = df[df['Region'] == region]
    if start:
        dff = dff[dff['Order Date'] >= start]
    if end:
        dff = dff[dff['Order Date'] <= end]
 
    by_cat = dff.groupby('Category', as_index=False)['Sales'].sum()
 
    return (
        px.bar(by_cat, x='Category', y='Sales'),
        px.line(dff, x='Order Date', y='Profit'),
        f'${dff["Sales"].sum():,.0f}'
    )
 
if __name__ == '__main__':
    app.run(debug=True)