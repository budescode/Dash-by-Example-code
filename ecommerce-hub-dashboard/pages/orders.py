"""Order detail table with an AG Grid."""
import dash
from dash import html
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from data_loader import df
 
dash.register_page(__name__, path='/orders', name='Orders')
 
# The raw orders behind the charts. A sortable,
# filterable grid; status colour-coded, payment as money.
 
# Colour the status cell by delivery outcome (JS).
status_style = {'function':
    "params.value==='delivered'"
    " ? {color:'#28a745',fontWeight:'bold'} :"
    "params.value==='cancelled'"
    " ? {color:'#dc3545',fontWeight:'bold'} :"
    "params.value==='shipped' ? {color:'#00B4D8'} : {}"}
 
money = {'function': 'd3.format("$,.2f")(params.value)'}
 
layout = dbc.Container([
    html.H4([html.I(className='bi bi-table me-2'),
             'Order Detail']),
    dag.AgGrid(
        id='orders-table',
        columnSize='responsiveSizeToFit',
        columnDefs=[
            {'field': 'order_id', 'width': 260,
             'pinned': 'left'},
            {'field': 'order_status', 'width': 130,
             'cellStyle': status_style},
            {'field': 'payment_value', 'width': 140,
             'valueFormatter': money},
            {'field': 'customer_state', 'width': 120},
            {'field': 'month', 'width': 110},
        ],
        rowData=df.to_dict('records'),
        defaultColDef={'sortable': True, 'filter': True,
                       'resizable': True},
        dashGridOptions={'pagination': True,
                         'paginationPageSize': 25},
        style={'height': '500px'},
    ),
])