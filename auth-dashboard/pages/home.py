"""Home page, visible only when logged in."""
 
import dash
from dash import html
from auth import login_required
 
dash.register_page(__name__, path="/")
 
@login_required   # guests are sent to /login
def layout():
    return html.Div("Home page")