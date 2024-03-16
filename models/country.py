from init import db, ma
from marshmallow import fields


# create database model for countries
class Country(db.Model):

    # define name and columns of the table
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    # establish relationship with other table
    itineraries = db.relationship("Itinerary", back_populates="country")

# create schema for country objects
class CountrySchema(ma.Schema):

    # use existing schema for the following fields
    itineraries = fields.List(fields.Nested("ItinerarySchema", only=["id"]))

    # define fields to be serialized
    class Meta:
        fields = ("id", "name", "itineraries")     

country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)
