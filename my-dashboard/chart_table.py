import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
 
df = pd.DataFrame({
    'Region':   ['North']*2 + ['South']*2 + ['East']*2,
    'Category': ['Furniture', 'Tech'] * 3,
    'Sales':    [1200, 1800, 900, 1500, 1100, 1700],
})
 
fig = px.bar(df, x='Category', y='Sales', color='Region',
             barmode='group', title='Sales by Category',
             template='plotly_white')
 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
 
app.layout = dbc.Container([
    html.H4('Sales Overview', className='mt-4'),
 
    dcc.Graph(figure=fig),
 
    html.H5('The data behind the chart', className='mt-4'),
    html.P("Every order in one sortable, filterable table. "
           "Status is colour coded and payment shown as "
           "currency, so you can drill into the orders behind "
           "the charts.",
           className='text-muted'),
    dag.AgGrid(
        rowData=df.to_dict('records'),
        columnDefs=[{'field': c} for c in df.columns],
        columnSize='responsiveSizeToFit',
        style={'height': 250},
    ),
], className='mb-5')
 
if __name__ == '__main__':
    app.run(debug=True)