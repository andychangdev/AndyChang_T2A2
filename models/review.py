from init import db, ma
from marshmallow import fields


# create database model for reviews
class Review(db.Model):

    # define name and columns of the table
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String)
    comment = db.Column(db.Text)
    date_posted = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey("itineraries.id"), nullable=False)

    # establish relationship with other table
    user = db.relationship("User", back_populates="reviews")
    itinerary = db.relationship("Itinerary", back_populates="reviews")


# create schema for review objects
class ReviewSchema(ma.Schema):

    # use existing schema for the following fields
    user = fields.Nested("UserSchema", only=["username"])
    itinerary = fields.Nested("ItinerarySchema", exclude=["reviews"])

    # define fields to be serialized
    class Meta:
        fields = ("id", "rating", "comment", "date_posted", "user", "itinerary")

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)