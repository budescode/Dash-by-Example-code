"""The users table: one class that Flask-SQLAlchemy turns into
a table, plus the password helpers every page uses."""
 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
 
db = SQLAlchemy()   # shared database object; app.py attaches it
 
 
class User(UserMixin, db.Model):
    """One row per account. UserMixin adds what Flask-Login needs:
    is_authenticated, is_active, is_anonymous and get_id()."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=True)  # nullable: social users later
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    provider = db.Column(db.String(20), nullable=True)      # "google", "github", or None
    avatar_url = db.Column(db.Text, nullable=True)
 
    @property
    def full_name(self):
        """Full name, or the email when both name fields are empty."""
        return " ".join(p for p in (self.first_name, self.last_name) if p) or self.email
 
    def set_password(self, password):
        """Store a salted hash of the password, never the password."""
        self.password_hash = generate_password_hash(password)
 
    def check_password(self, password):
        """True if the password matches the stored hash; False for an
        account with no password yet (social sign-in only)."""
        return bool(self.password_hash) and check_password_hash(self.password_hash, password)