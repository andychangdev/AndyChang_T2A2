from init import db, ma
from marshmallow import fields


# create database model for destinations
class Destination(db.Model):

    # define name and columns of the table
    __tablename__ = "destinations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    type = db.Column(db.String, nullable=False)

    # establish relationship with other table
    itineraries = db.relationship("Itinerary", back_populates="destination")

# create schema for destination objects
class DestinationSchema(ma.Schema):

    # use existing schema for the following fields
    itineraries = fields.List(fields.Nested("ItinerarySchema", only=["id"]))

    # define fields to be serialized
    class Meta:
        fields = ("id", "name", "type", "itineraries")     

destination_schema = DestinationSchema()
destinations_schema = DestinationSchema(many=True)
