from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
import re

# Initialize SQLAlchemy
db = SQLAlchemy()

class UserRegistrationModel(db.Model):
    __tablename__ = 'user_registration'

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    name = db.Column(db.String(100), nullable=False)  # Name
    loginid = db.Column(db.String(100), nullable=False)  # Login ID (unique)
    password = db.Column(db.String(100), nullable=False)  # Password
    mobile = db.Column(db.String(10), nullable=False, unique=True)  # Mobile (unique)
    email = db.Column(db.String(100), nullable=False, unique=True)  # Email (unique)
    locality = db.Column(db.String(100), nullable=False)  # Locality
    state = db.Column(db.Text, nullable=False)  # Address
    status = db.Column(db.String(100), default='waiting')  # Status

    def __repr__(self):
        return f"<UserRegistrationModel {self.name}>"
    

# Validation via event listeners
@event.listens_for(UserRegistrationModel, 'before_insert')
def validate_user_registration(mapper, connection, target):
    # Validate name (only letters)
    if not re.match(r'^[a-zA-Z\s    ]+$', target.name):
        raise ValueError("Name must contain only letters")

    # Validate loginid (only letters)
    if not re.match(r'^[a-zA-Z]+$', target.loginid):
        raise ValueError("Login ID must contain only letters")

    # Validate password (at least one digit, one uppercase, one lowercase, and minimum 8 characters)
    if not re.match(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}', target.password):
        raise ValueError("Password must contain at least one number, one uppercase letter, one lowercase letter, and at least 8 characters")

    # Validate mobile number (starts with 6, 7, 8, or 9, and is 10 digits long)
    if not re.match(r'^[6789]\d{9}$', target.mobile):
        raise ValueError("Mobile must start with 6, 7, 8, or 9 and be 10 digits long")

    # Validate email format
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', target.email):
        raise ValueError("Enter a valid email address")

# This method allows Flask-SQLAlchemy to enforce validation when inserting a new user.
