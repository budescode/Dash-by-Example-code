import dash
from dash import html
import dash_bootstrap_components as dbc
 
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.FLATLY, dbc.icons.BOOTSTRAP])
 
def chip(label, color='primary'):
    return html.Div(label, className=f'bg-{color} text-white px-3 py-2 rounded')
 
def label(text):
    return html.H6(text, className='text-muted mt-4')
 
app.layout = dbc.Container([
    html.H4('Flexbox utilities', className='my-3'),
 
    # Title on the left, action buttons pushed to the right
    label('justify-content-between: title left, actions pushed right'),
    html.Div([
        html.H5('Order Detail', className='mb-0'),
        html.Div([
            dbc.Button('Export', size='sm', color='secondary', className='me-2'),
            dbc.Button('Refresh', size='sm', color='primary'),
        ]),
    ], className='d-flex justify-content-between align-items-center border rounded p-2'),
 
    # Centre a value and its icon both horizontally and vertically
    label('justify-content-center + align-items-center: centred both ways'),
    html.Div([
        html.I(className='bi bi-currency-dollar fs-3 me-2'),
        html.H3('$2,297,201', className='mb-0'),
    ], className='d-flex justify-content-center align-items-center border rounded p-3'),
 
    # Every justify-content option, each row labelled with what it does
    label('justify-content-*: how items spread across the row'),
    *[html.Div([
        html.Small(f'justify-content-{j}: {desc}', className='text-muted'),
        html.Div([chip('A'), chip('B'), chip('C')],
                 className=f'd-flex justify-content-{j} border rounded p-2'),
    ], className='mb-3')
      for j, desc in [
          ('start',   'items packed to the left'),
          ('center',  'items grouped in the middle'),
          ('end',     'items packed to the right'),
          ('between', 'first and last on the edges, equal space between'),
          ('around',  'equal space around each item'),
          ('evenly',  'equal space between items and at both ends'),
      ]],
 
    # Different-height items lined up on their centres
    label('align-items-center: different-height items share a centre line'),
    html.Div([
        html.Div('short',      className='bg-primary text-white p-2 rounded'),
        html.Div('taller box', className='bg-success text-white p-4 rounded'),
        html.Div('short',      className='bg-danger text-white p-2 rounded'),
    ], className='d-flex align-items-center gap-2 border rounded p-2'),
 
    # ms-auto eats the leftover space and shoves one item to the right
    label('ms-auto: push one item to the far right'),
    html.Div([
        chip('Logo'),
        chip('Menu', 'secondary'),
        dbc.Button('Sign in', size='sm', className='ms-auto'),
    ], className='d-flex align-items-center gap-2 border rounded p-2'),
 
    # Stack vertically instead of in a row
    label('flex-column: stack items vertically instead of in a row'),
    html.Div([chip('Row 1'), chip('Row 2'), chip('Row 3')],
             className='d-flex flex-column gap-2 border rounded p-2'),
 
], fluid=True, className='mb-5')
 
if __name__ == '__main__':
    app.run(debug=True)