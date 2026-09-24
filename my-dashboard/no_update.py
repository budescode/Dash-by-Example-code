import dash
from dash import html, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
import pandas as pd
 
df = pd.DataFrame({
    'Product Name': ['Blue Chair', 'Red Desk',
                     'Blue Lamp', 'Green Sofa'],
    'Sales':        [120, 340, 90, 560],
})
 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
 
app.layout = dbc.Container([
    html.P('Press Search with the box empty: the message changes but '
           'the results stay. Type a colour and press again.',
           className='text-muted mt-3'),
    dbc.Input(id='search-input',
              placeholder='Search products, e.g. red, blue, green',
              type='text'),
    dbc.Button('Search', id='search-btn', color='primary',
               className='mt-2'),
    html.P(id='message', className='text-danger mt-2'),
    html.Pre(id='results', className='mt-2'),
])
 
@callback(
    Output('results', 'children'),
    Output('message', 'children'),
    Input('search-btn', 'n_clicks'),
    State('search-input', 'value'),
    prevent_initial_call=True
)
def search(n_clicks, query):
    if not query:
        # Leave the results as they are; only the message changes.
        return no_update, 'Type something first.'
    hits = df[df['Product Name'].str.contains(query, case=False)]
    return hits.to_string(index=False), ''
 
if __name__ == '__main__':
    app.run(debug=True)