"""Login page: checks the password and starts the session."""
 
import dash
from dash import html, dcc, Input, Output, State, no_update, callback
import dash_bootstrap_components as dbc
from models import db, User
from flask_login import login_user
 
dash.register_page(__name__, path="/login")   # the URL
 
def layout():
    """Email and password form; refresh=True forces a full reload."""
    return dbc.Container(dbc.Row(dbc.Col(md={"size": 6, "offset": 3}, children=[
        html.H2("Login", className="mb-3"),
        dbc.Input(placeholder="Email", id="login-email", type="email", className="mb-3"),
        dbc.Input(type="password", id="login-password", placeholder="Password", className="mb-3"),
        dbc.Button("Submit", id="login-btn", className="btn btn-primary", n_clicks=0),
        html.P("", id="login-msg", style={"color": "red"}),
        # refresh=True: full reload, so the navbar sees the login

            # external_link=True: a real page load, so Flask serves the route
    dbc.Button("Continue with Google", href="/auth/start?provider=google",
               color="light", className="mb-2 w-100",
               external_link=True),
    dbc.Button("Continue with GitHub", href="/auth/start?provider=github",
               color="dark", className="mb-3 w-100",
               external_link=True),
    html.Hr(),
    
        dcc.Location(id="login-redirect", refresh=True),
    ])), className="mt-3")
 
# Runs when Submit is clicked
@callback(
    Output("login-redirect", "href"),
    Output("login-msg", "children"),
    Input("login-btn", "n_clicks"),
    State("login-email", "value"), State("login-password", "value"),
    # do not run when the page first loads
    prevent_initial_call=True,
)
def perform_login(n_clicks, email, password):
    """Look the user up, check the password, start the session."""
    if not email or not password:
        return no_update, "Enter email and password."
 
    # find the account by email
    user = db.session.execute(
        db.select(User).where(User.email == email.strip().lower())
    ).scalar_one_or_none()
    # one message for both cases, so nobody learns which was wrong
    if user is None or not user.check_password(password):
        return no_update, "Invalid email or password."
 
    login_user(user)   # Flask-Login sets the session cookie
    return "/profile", ""