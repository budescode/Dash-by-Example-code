import dash
from dash import html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
 
df = pd.DataFrame({
    'Product Name': ['Blue Chair', 'Red Desk', 'Blue Lamp', 'Green Sofa'],
    'Sales':        [120, 340, 90, 560],
})
 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
 
app.layout = dbc.Container([
    html.P('Type a colour, then press Search. Typing alone changes '
           'nothing; only the button triggers the callback.',
           className='text-muted mt-3'),
    dbc.Input(id='search-input',
              placeholder='Search products, e.g. red, blue, green',
              type='text', className='mt-3'),
    dbc.Button('Search', id='search-btn', color='primary',
               className='mt-2'),
    html.Pre(id='results', className='mt-3'),
])
 
@callback(
    Output('results', 'children'),
    Input('search-btn', 'n_clicks'),
    State('search-input', 'value'),
    prevent_initial_call=True
)
def search(n_clicks, query):
    if not query:
        return 'Type something, then press Search.'
    hits = df[df['Product Name'].str.contains(query, case=False)]
    return hits.to_string(index=False)
 
if __name__ == '__main__':
    app.run(debug=True)