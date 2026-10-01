"""Logout page: ends the session and returns to /login."""
import dash
from dash import dcc
from flask_login import logout_user
 
dash.register_page(__name__, path="/logout")
 
def layout():
    """Visiting the page is the action; there is nothing to click."""
    logout_user()   # clears the session cookie
    return dcc.Location(href="/login", id="logout-redirect")