import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
 
df = pd.DataFrame({
    'Region':   ['North']*2 + ['South']*2 + ['East']*2,
    'Category': ['Furniture', 'Tech'] * 3,
    'Sales':    [1200, 1800, 900, 1500, 1100, 1700],
})
print(df)
 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
 
app.layout = dbc.Container([
    html.H4('Sales by Region', className='mt-3'),
    html.P('Select a region and watch the chart change.',
           className='text-muted'),
    dcc.Dropdown(
        id='region-filter',
        options=[{'label': r, 'value': r} for r in df['Region'].unique()],
        value='North',
        clearable=False
    ),
    dcc.Graph(id='sales-chart')
])
 
@callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(selected_region):
    filtered_df = df[df['Region'] == selected_region]
    fig = px.bar(filtered_df, x='Category', y='Sales',
                 title=f'{selected_region} Sales')
    return fig
 
if __name__ == '__main__':
    app.run(debug=True)