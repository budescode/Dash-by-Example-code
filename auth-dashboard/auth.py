"""Helpers shared by every page: login_required, reset tokens."""
 
from functools import wraps
from dash import dcc
from flask_login import current_user
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from models import db, User
from flask import current_app
 
def login_required(layout_fn):
    """Wrap a page's layout(): guests get sent to /login instead."""
    # wraps keeps the original function name for Dash
    @wraps(layout_fn)
    def wrapper(*args, **kwargs):
        # guest: send to the login page instead
        if not current_user.is_authenticated:
            return dcc.Location(href="/login", id="auth-redirect", refresh=True)
        # logged in: show the page as normal
        return layout_fn(*args, **kwargs)
    return wrapper

def make_reset_token(user):
    """Signed token holding the user id. A slice of the password hash
    makes it single-use: it stops matching once the password changes."""
    # signed with SECRET_KEY, so nobody can forge or edit the token
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="password-reset")
    # the token carries the id and the last 8 chars of the hash
    return s.dumps({"id": user.id, "ph": (user.password_hash or "")[-8:]})
 
def verify_reset_token(token, max_age=3600):
    """The User for a valid, unexpired token, otherwise None."""
    # must match make_reset_token exactly
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="password-reset")
    try:
        # fails if the signature is wrong or the token is too old
        data = s.loads(token, max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None
    user = db.session.get(User, data["id"])   # fetch by id
    # hash changed: the token was already used
    if user is None or (user.password_hash or "")[-8:] != data["ph"]:
        return None
    return user

def save_or_update_user(profile, provider, avatar_url=None):
    """Find the account by email, or create it, then store the
    provider details. Both sign-in methods share one row."""
    email = profile["email"].strip().lower()
    user = db.session.execute(
        db.select(User).where(User.email == email)
    ).scalar_one_or_none()
 
    if user is None:   # first visit: create the account
        user = User(
            email=email,
            first_name=profile.get("given_name") or profile.get("name"),
            last_name=profile.get("family_name"),
            password_hash=None,   # no password yet, OAuth-only account
        )
        db.session.add(user)
 
    user.provider = provider   # remember which provider
    user.avatar_url = avatar_url   # None if the provider sent none
    db.session.commit()
    return user