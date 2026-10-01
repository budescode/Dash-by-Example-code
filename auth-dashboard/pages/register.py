"""Register page: a form that creates a new User."""
 
import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
from models import db, User
from sqlalchemy.exc import IntegrityError
 
dash.register_page(__name__, path="/register")   # the URL
 
def layout():
    """The form. dcc.Location is how the callback redirects."""
    return dbc.Container(
        dbc.Row(dbc.Col(md={"size": 6, "offset": 3}, children=[
            html.H2("Register", className="mb-3"),
            # the form fields; the callback reads them as State
            dbc.Input(placeholder="Firstname", id="register-firstname", className="mb-3"),
            dbc.Input(placeholder="Lastname", id="register-lastname", className="mb-3"),
            dbc.Input(placeholder="Email", id="register-email", type="email", className="mb-3"),
            dbc.Input(type="password", id="register-password", placeholder="Password", className="mb-3"),
            # clicking Submit fires the callback
            dbc.Button("Submit", id="register-btn", className="btn btn-primary", n_clicks=0),
            # error messages show here
            html.P("", id="register-msg", style={"color": "red"}),
            # setting its href sends the browser to another page
            dcc.Location(id="register-redirect"),
        ])), className="mt-3",
    )
 
# Two outputs.
@callback(
    Output("register-redirect", "href"),
    Output("register-msg", "children"),
    Input("register-btn", "n_clicks"),
    State("register-firstname", "value"), State("register-lastname", "value"),
    State("register-email", "value"), State("register-password", "value"),
    # do not run when the page first loads
    prevent_initial_call=True,
)
def register_user(n_clicks, firstname, lastname, email, password):
    """Validate, check the email is free, hash the password, save."""
    # every field must be filled
    if not all([firstname, lastname, email, password]):
        return no_update, "Enter valid details"
 
    email = email.strip().lower()   # trim spaces, lowercase
    # is this email already taken?
    exists = db.session.execute(
        db.select(User).where(User.email == email)
    ).scalar_one_or_none()
    if exists:
        return no_update, "A user with this email exists already"
 
    # build the row; set_password stores a hash, not the password
    user = User(email=email, first_name=firstname, last_name=lastname)
    user.set_password(password)
    # save it, then send the browser to the login page
    try:
        db.session.add(user)
        db.session.commit()
        return "/login", ""
    except IntegrityError:   # same email was saved a moment ago
        db.session.rollback()
        return no_update, "A user with this email exists already"