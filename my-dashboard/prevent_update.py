import dash
from dash import dcc, html, Input, Output, ctx, callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
 
dates = pd.date_range(end='today', periods=365)
df = pd.DataFrame({'date': dates,
                   'value': np.random.randn(365).cumsum() + 100})
 
def build_chart(days):
    dff = df.tail(days)
    return px.line(dff, x='date', y='value',
                   title=f'Last {days} days')
 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
 
app.layout = dbc.Container([
    html.P('Press Week or Month to draw the chart. Year does nothing '
           'on purpose: the callback raises PreventUpdate.',
           className='text-muted mt-3'),
    dbc.ButtonGroup([
        dbc.Button('Week',  id='btn-week'),
        dbc.Button('Month', id='btn-month'),
        dbc.Button('Year',  id='btn-year'),
    ], className='mt-3'),
    dcc.Graph(id='chart'),
])
 
@callback(
    Output('chart', 'figure'),
    Input('btn-week',  'n_clicks'),
    Input('btn-month', 'n_clicks'),
    Input('btn-year',  'n_clicks'),
)
def on_period_btn(w, m, y):
    if ctx.triggered_id == 'btn-week':
        return build_chart(7)
    if ctx.triggered_id == 'btn-month':
        return build_chart(30)
    # Page load, or the Year button: leave the chart as it is.
    raise PreventUpdate
 
if __name__ == '__main__':
    app.run(debug=True)