import os
import dash
from dash import html
 
app = dash.Dash(__name__)
server = app.server
 
app.layout = html.Div("Hello from Dash!")
 
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(debug=True, host='0.0.0.0', port=port)