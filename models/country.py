from init import db, ma
from marshmallow import fields

# create database that represents the user entity
class Country(db.Model):
    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    itineraries = db.relationship("Itinerary", back_populates="country")

# creates a schema for user object
class CountrySchema(ma.Schema):
    itineraries = fields.List(fields.Nested('ItinerarySchema', exclude=['country']))

    class Meta:
        fields = ("id", "name")


user_schema = CountrySchema()
users_schema = CountrySchema(many=True)
