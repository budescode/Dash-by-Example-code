"""Change Password page, reached from the emailed link."""
import dash
from dash import html, dcc, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
from models import db, User
from auth import verify_reset_token
 
# <token> in the URL becomes the token argument of layout()
dash.register_page(__name__, path_template="/change-password/<token>")
 
def layout(token=None, **kwargs):
    """Show the form only if the token in the URL is valid."""
    if verify_reset_token(token) is None:
        return html.Div("The link is invalid or expired")
    return dbc.Container(dbc.Row(dbc.Col(md={"size": 6, "offset": 3}, children=[
        html.H2("Change Password", className="mb-3"),
        dbc.Input(type="password", id="change-password", placeholder="New password", className="mb-3"),
        dbc.Button("Submit", id="change-btn", className="btn btn-primary", n_clicks=0),
        html.P("", id="change-msg", style={"color": "red"}),
        dcc.Location(id="change-redirect", refresh=True),
        # the token travels from the URL to the callback via a Store
        dcc.Store(id="cp-token", data=token),
    ])), className="mt-3")
 
# Runs when Submit is clicked
@callback(
    Output("change-redirect", "href"), Output("change-msg", "children"),
    Input("change-btn", "n_clicks"),
    State("change-password", "value"), State("cp-token", "data"),
    prevent_initial_call=True,
)
def perform_change(n_clicks, password, token):
    """Check the token again, then save the new password."""
    user = verify_reset_token(token)
    if user is None:
        return no_update, "The link is invalid or expired"
    user.set_password(password)   # hash and store it
    db.session.commit()
    return "/login", ""   # back to login