# pages/orders.py
import dash
from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
from data_loader import filter_df
 
dash.register_page(__name__, path='/orders', name='Order Detail')
 
layout = dbc.Container([
    dbc.Card([
        dbc.CardHeader([
            html.I(className='bi bi-table me-2'),
            html.Span('Order Detail', className='fw-bold')
        ]),
        dbc.CardBody(dag.AgGrid(
            id='orders-grid',
            # stretch columns to fill the width
            columnSize='responsiveSizeToFit',
            # one dict per column: field, pinning, formatting
            columnDefs=[
                {'field':'Order ID', 'pinned':'left'},
                {'field':'Order Date'},
                {'field':'Customer Name'},
                {'field':'Region'},
                {'field':'Category'},
                {'field':'Sub-Category'},
                {'field':'Sales', 'valueFormatter':{
                    'function':'d3.format("$,.2f")(params.value)'}},
                {'field':'Profit', 'valueFormatter':{
                    'function':'d3.format("$,.2f")(params.value)'}},
                {'field':'Quantity'},
            ],
            rowData=[],
            defaultColDef={'sortable':True,'filter':True,'resizable':True},
            dashGridOptions={'pagination': True,
                             'paginationPageSize': 20},
            style={'height':'500px'},
        ))
    ]),
], fluid=True)
 
@callback(
    Output('orders-grid', 'rowData'),
    Input('filtered-store', 'data'),
)
def update_orders(filters):
    """Feed the filtered records straight into the grid; the grid
    handles sorting, filtering and pagination on its own."""
    return filter_df(filters).to_dict('records')