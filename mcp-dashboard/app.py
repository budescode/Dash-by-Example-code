import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
 
df = pd.DataFrame({
    'month':  ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    'sales':  [120, 145, 130, 160, 175, 190],
    'region': ['North', 'North', 'South', 'South', 'East', 'East'],
})
 
app = Dash(__name__, enable_mcp=True)
server = app.server
 
app.layout = html.Div([
    dcc.Dropdown(
        id='region',
        options=[{'label': r, 'value': r}
                 for r in df['region'].unique()],
        value='North',
    ),
    dcc.Graph(id='chart'),
])
 
@callback(Output('chart', 'figure'), Input('region', 'value'))
def update_chart(region):
    """Return a bar chart of monthly sales for the selected region."""
    filtered = df[df['region'] == region]
    return px.bar(filtered, x='month', y='sales',
                  title=f'Sales - {region}')
 
if __name__ == '__main__':
    app.run(debug=True)