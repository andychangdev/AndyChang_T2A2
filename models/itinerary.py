from init import db, ma
from marshmallow import fields


# create database that represents the itinerary entity
class Itinerary(db.Model):
    __tablename__ = "itineraries"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    date_posted = db.Column(db.Date)
    duration = db.Column(db.String(10))
    post_type = db.Column(db.String(10))
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    country = db.relationship("Country", back_populates="itineraries")
    user = db.relationship("User", back_populates="itineraries")


# creates a schema for user object
class ItinerarySchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["username"])
    country = fields.Nested("CountrySchema", only=["name"])

    class Meta:
        fields = ("id", "title", "content", "date_posted", "duration", "post_type", "country", "user",)
        ordered = True

itinerary_schema = ItinerarySchema()
itineraries_schema = ItinerarySchema(many=True)
