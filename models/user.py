from init import db, ma
from marshmallow import fields


# create database model for users
class User(db.Model):

    # define name and columns of the table
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_joined = db.Column(db.Date, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # establish relationship with other table
    itineraries = db.relationship("Itinerary", back_populates="user", cascade="all, delete")
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete")


# create a schema for user object
class UserSchema(ma.Schema):

    # use existing schema for the following fields
    itineraries = fields.List(fields.Nested("ItinerarySchema", exclude=["user"]))
    reviews = fields.List(fields.Nested("ReviewSchema", exclude=["user"]))

    # define fields to be serialized
    class Meta:
        fields = ("id", "username", "email", "password", "date_joined", "is_admin", "itineraries", "reviews")

user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])
