"""Profile page: shows the logged-in user's details."""
import dash
import dash_bootstrap_components as dbc
from flask_login import current_user
from auth import login_required
 
dash.register_page(__name__, path="/profile")
 
@login_required
def layout():
    return dbc.Container(dbc.Row(dbc.Col(md={"size": 6, "offset": 3}, children=[
        # current_user is the logged-in User from Flask-Login
        dbc.ListGroup([
            dbc.ListGroupItem("User Details", active=True),
            dbc.ListGroupItem(f"Firstname: {current_user.first_name}"),
            dbc.ListGroupItem(f"Lastname: {current_user.last_name}"),
            dbc.ListGroupItem(f"Email: {current_user.email}"),
        ]),
    ])), className="mt-3")