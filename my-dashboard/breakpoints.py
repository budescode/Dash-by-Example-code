import dash
from dash import html
import dash_bootstrap_components as dbc
 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
 
def kpi_card(title, value, color):
    return dbc.Card(
        dbc.CardBody([
            html.P(title, className='text-muted mb-1', style={'fontSize': '0.8rem'}),
            html.H3(value, className='fw-bold mb-0', style={'color': color}),
        ]),
        style={'borderLeft': f'5px solid {color}'},
        className='shadow-sm h-100',
    )
 
# Build the three cards with distinct colours so rows are easy to tell apart
kpi_revenue = kpi_card('Total Revenue', '$128,400', 'blue')
kpi_orders  = kpi_card('Total Orders',  '1,204',    'green')
kpi_profit  = kpi_card('Net Profit',    '$22,150',  'orange')
 
app.layout = dbc.Container([
    html.P('Resize the browser window: one card per row on a phone, '
           'two on a tablet, three on a desktop.',
           className='text-muted mt-3'),
    dbc.Row([
        # Full width on phones, half on tablets, a third on desktop
        dbc.Col(kpi_revenue, xs=12, sm=6, md=4),
        dbc.Col(kpi_orders,  xs=12, sm=6, md=4),
        dbc.Col(kpi_profit,  xs=12, sm=12, md=4),
    ], className='g-3 mt-3'),
], fluid=True)
 
if __name__ == '__main__':
    app.run(debug=True)