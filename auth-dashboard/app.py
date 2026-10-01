"""Creates the Dash app, connects the database and
Flask-Login, and builds the navbar around the pages."""
 
from dash import Dash, html, page_container
import dash_bootstrap_components as dbc
import os
from dotenv import load_dotenv
from models import db, User
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
import secrets
from flask import request, redirect, session
from flask_login import login_user
from auth import save_or_update_user
from dash_social_signin import (
    build_authorize_url, build_pkce_verifier, build_pkce_challenge,
    verify_oauth_callback,
)

load_dotenv()   # read .env into os.environ
# use_pages=True: every file in pages/ becomes a route
app = Dash(__name__, title="Authentication Tutorial", use_pages=True,
           suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # exposed for production servers, e.g. gunicorn app:server
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
server.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{os.path.join(BASE_DIR, 'users.db')}",
)
# SECRET_KEY signs the session cookie and the reset tokens
server.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
# BASE_URL builds the link in the forgot-password email
server.config["BASE_URL"] = os.environ.get("BASE_URL", "http://localhost:8050")
 
db.init_app(server)               # connect models.py to the app
# Migrate adds the "flask db" commands that update the tables.
# render_as_batch=True: SQLite cannot alter a column in place,
# so each migration rebuilds the table instead.
migrate = Migrate(server, db, render_as_batch=True)
login_manager = LoginManager(server)   # session cookie handling
login_manager.login_view = "/login"    # where guests are sent
 
# ids and secrets from .env; scope is what we ask to read
PROVIDERS = {
    "google": {
        "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
        "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
        "scope": "openid email profile",
    },
    "github": {
        "client_id": os.environ.get("GITHUB_CLIENT_ID"),
        "client_secret": os.environ.get("GITHUB_CLIENT_SECRET"),
        "scope": "read:user user:email",
    },
}

 
# Step 1: send the browser to Google or GitHub to sign in
@server.route("/auth/start")
def auth_start():
    provider = request.args.get("provider")
    cfg = PROVIDERS[provider]
    # a one-time secret that proves the reply is for this app
    verifier = build_pkce_verifier()
    state = secrets.token_urlsafe(16)   # random, checked on return
    # kept in the session cookie until the provider sends us back
    session["oauth_provider"] = provider
    session["oauth_verifier"] = verifier
    session["oauth_state"] = state
    url = build_authorize_url(
        provider,
        client_id=cfg["client_id"],
        redirect_uri=f'{server.config["BASE_URL"]}/auth/callback',
        scope=cfg["scope"],
        state=state,
        code_challenge=build_pkce_challenge(verifier),
    )
    return redirect(url)   # off to the provider's login page
 
# Step 2: the provider sends the browser back here with a code
@server.route("/auth/callback")
def auth_callback():
    # read back what step 1 saved
    provider = session.pop("oauth_provider", None)
    verifier = session.pop("oauth_verifier", None)
    state = session.pop("oauth_state", None)
    if not state or request.args.get("state") != state:  # tampered?
        return "Invalid state parameter", 400
    cfg = PROVIDERS[provider]
    # swap the code for tokens and the user's profile
    tokens, profile = verify_oauth_callback(
        provider,
        code=request.args.get("code"),
        redirect_uri=f'{server.config["BASE_URL"]}/auth/callback',
        client_id=cfg["client_id"],
        client_secret=cfg["client_secret"],
        code_verifier=verifier,
    )
    # Google sends "picture", GitHub sends "avatar_url"
    picture = profile.get("picture") or profile.get("avatar_url")
    user = save_or_update_user(profile, provider, avatar_url=picture)
    login_user(user)   # same session cookie as the password login
    return redirect("/profile")


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login calls this on every request to turn the id in
    the session cookie back into a User object."""
    return db.session.get(User, int(user_id))
 
 
def app_layout():
    """Built on every page load, so the navbar follows the login."""
    navitem = [dbc.NavItem(dbc.NavLink("Home", href="/", active="exact"))]
    if current_user.is_authenticated:
        navitem.append(dbc.NavItem(dbc.NavLink("Profile", href="/profile", active="exact")))
        navitem.append(dbc.NavItem(dbc.NavLink("Logout", href="/logout", active="exact")))
    else:
        navitem.append(dbc.NavItem(dbc.NavLink("Register", href="/register", active="exact")))
        navitem.append(dbc.NavItem(dbc.NavLink("Login", href="/login", active="exact")))
        navitem.append(dbc.NavItem(dbc.NavLink("Reset Password", href="/reset-password", active="exact")))
 
    return dbc.Container(
        [
            dbc.NavbarSimple(children=navitem, brand="Authentication", brand_href="/",
                              color="primary", dark=True),
            page_container,
        ],
        fluid=True, className="p-0 m-0",
    )
 
 
app.layout = app_layout   # a function, so it runs on every load
 
if __name__ == "__main__":
    app.run(debug=True)