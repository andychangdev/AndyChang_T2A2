from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf


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

    # validates destination name
    name = fields.String(
        required=True, validate=And(
            Length(min=4, max=30, error="Destination name must be between 4 and 30 characters long"),
            Regexp("^[a-zA-Z ]+$", error="Destination name can only contain letters")
        ),
    )
    # validates destination type
    type = fields.String(validate=OneOf(["Country", "City"], error='Destination type must be either "Country" or "City"'))

    # define fields to be serialized
    class Meta:
        fields = ("name", "type")     

destination_schema = DestinationSchema()
destinations_schema = DestinationSchema(many=True)
