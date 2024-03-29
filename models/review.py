from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp, OneOf


# create database model for reviews
class Review(db.Model):

    # define name of the table
    __tablename__ = "reviews"

    # define columns of the table
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    content = db.Column(db.Text)
    date_posted = db.Column(db.Date)
    
    # define foreign keys of the table
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey("itineraries.id"), nullable=False)

    # establish relationship with other table
    user = db.relationship("User", back_populates="reviews")
    itinerary = db.relationship("Itinerary", back_populates="reviews")


# create schema for review objects
class ReviewSchema(ma.Schema):

    # validates rating
    rating = fields.Integer(
        validate=OneOf([1, 2, 3, 4, 5], error="Rating must be a number between 1 and 5"))
    
    # validates content
    content = fields.String(
        required=True,
        validate=Regexp("^[a-zA-Z0-9 ]+$", error="Content can only contain alphanumeric characters"))
    
    # use existing schema for the following fields
    user = fields.Nested("UserSchema", only=["username"])
    itinerary = fields.Nested("ItinerarySchema", exclude=["reviews"])

    # define fields to be serialised and deserialised
    class Meta:
        fields = ("id", "rating", "content", "date_posted", "user", "itinerary")


# create a schema instance for serialising and deserialising a single and multiple review
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True, exclude=["itinerary"])