from init import db, ma
from marshmallow import fields


# create database that represents the itinerary entity
class Itinerary(db.Model):
    __tablename__ = "itineraries"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    date = db.Column(db.Date)
    duration = db.Column(db.String(10))
    type = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    user = db.relationship("User", back_populates="itineraries")


# creates a schema for user object
class ItinerarySchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["username"])

    class Meta:
        fields = ("id", "title", "content", "date", "duration", "type", "user")


itinerary_schema = ItinerarySchema()
itineraries_schema = ItinerarySchema(many=True)
