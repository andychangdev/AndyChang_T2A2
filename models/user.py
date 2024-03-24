from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

# Create database model for users
class User(db.Model):

    # define name of the table
    __tablename__ = "users"
    
    # define columns of the table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_joined = db.Column(db.Date, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # establish relationship with other table
    itineraries = db.relationship("Itinerary", back_populates="user", cascade="all, delete")
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete")


# Create schema for user objects
class UserSchema(ma.Schema):

    # validates username
    username = fields.String(
        required=False, validate=And(
            Length(min=4, max=20, error="Username must be between 4 and 20 characters long"),
            Regexp("^[a-zA-Z0-9_-]+$", error="Username can only contain letters, numbers, underscores, and hyphens.")
        ),
    )

    # validates username
    email = fields.String(
        required=True, validate=And(
            Length(min=10, max=254, error="Email address must be between 10 and 254 characters long"),
            Regexp("^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", error="Email addresses can only contain letters, numbers, periods, hyphens, and underscores")
        ),
    )

    # use existing schema for the following fields
    itineraries = fields.List(fields.Nested("ItinerarySchema", exclude=["user", "reviews"]))
    reviews = fields.List(fields.Nested("ReviewSchema", exclude=["user", "itinerary"]))

    # define fields to be serialised and deserialised
    class Meta:
        fields = ("id", "username", "email", "date_joined", "is_admin", "itineraries", "reviews")


# create a schema instance for serialising and deserialising a single and multiple user
user_schema = UserSchema()
users_schema = UserSchema(many=True, exclude=["itineraries", "reviews"])