"""Reset Password page: emails a signed link to the account."""
import dash
from dash import html, dcc, Input, Output, State, no_update, callback
import dash_bootstrap_components as dbc
from models import db, User
from auth import make_reset_token
from flask import current_app
from utils import send_email
 
dash.register_page(__name__, path="/reset-password")
 
def layout():
    """One email box; the reply text shows below it."""
    return dbc.Container(dbc.Row(dbc.Col(md={"size": 6, "offset": 3}, children=[
        html.H2("Reset Password", className="mb-3"),
        dbc.Input(placeholder="Email", id="reset-email", type="email", className="mb-3"),
        dbc.Button("Submit", id="reset-btn", className="btn btn-primary", n_clicks=0),
        html.P("", id="reset-msg", style={"color": "red"}),
    ])), className="mt-3")
 
# Runs when Submit is clicked
@callback(
    Output("reset-msg", "children"), Output("reset-msg", "style"),
    Input("reset-btn", "n_clicks"), State("reset-email", "value"),
    prevent_initial_call=True,
)
def perform_reset(n_clicks, email):
    """Email the link if the account exists. Same reply either way,
    so the form cannot be used to check which emails exist."""
    if not email:
        return "Enter an email.", no_update
 
    # find the account by email
    user = db.session.execute(
        db.select(User).where(User.email == email.strip().lower())
    ).scalar_one_or_none()
    if user is not None:   # only email real accounts
        token = make_reset_token(user)
        # the link opens the change-password page with the token
        url = f'{current_app.config["BASE_URL"]}/change-password/{token}'
        send_email("Reset Password", f"Reset your password: {url}", [email])
 
    # same reply whether or not the account exists
    return "Email has been sent if there is an account.", {"color": "green"}