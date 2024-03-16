from init import db, ma
from marshmallow import fields


# create database model for itineraries
class Itinerary(db.Model):

     # define name and columns of the table
    __tablename__ = "itineraries"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    date_posted = db.Column(db.Date)
    duration = db.Column(db.String(10))
    post_type = db.Column(db.String(10))
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    # establish relationship with other tables
    country = db.relationship("Country", back_populates="itineraries")
    user = db.relationship("User", back_populates="itineraries")
    reviews = db.relationship("Review", back_populates="itinerary")


# create schema for itinerary objects
class ItinerarySchema(ma.Schema):
    
    # use existing schemas for the following fields
    user = fields.Nested("UserSchema", only=["username"])
    country = fields.Nested("CountrySchema", only=["name"])
    reviews = fields.List(fields.Nested("ReviewSchema", exclude=["itinerary"]))

    # define fields to be serialized
    class Meta:
        fields = ("id", "title", "content", "date_posted", "duration", "post_type", "country", "user", "reviews")
        ordered = True # maintain order of the fields

itinerary_schema = ItinerarySchema()
itineraries_schema = ItinerarySchema(many=True)
