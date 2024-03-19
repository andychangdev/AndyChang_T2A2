from init import db, ma
from marshmallow import fields


# create database model for destinations
class Destination(db.Model):

    # define name and columns of the table
    __tablename__ = "destinations"
    # id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, primary_key=True)
    type = db.Column(db.String, nullable=False)

    # establish relationship with other table
    itineraries = db.relationship("Itinerary", back_populates="destination")

# create schema for destination objects
class DestinationSchema(ma.Schema):

    # define fields to be serialized
    class Meta:
        fields = ("name", "type")     

destination_schema = DestinationSchema()
destinations_schema = DestinationSchema(many=True)
