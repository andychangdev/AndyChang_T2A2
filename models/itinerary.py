from init import db, ma
from marshmallow import fields, ValidationError, validates
from marshmallow.validate import Length, And, Regexp, OneOf


# create database model for itineraries
class Itinerary(db.Model):

    # define name of the table
    __tablename__ = "itineraries"

    # define columns of the table
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    date_posted = db.Column(db.Date)
    duration = db.Column(db.String(10))
    post_type = db.Column(db.String)

    # define foreign keys of the table
    destination_name = db.Column(db.String, db.ForeignKey("destinations.name"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # establish relationship with other tables
    destination = db.relationship("Destination", back_populates="itineraries")
    user = db.relationship("User", back_populates="itineraries")
    reviews = db.relationship("Review", back_populates="itinerary", cascade='all, delete')


# create schema for itinerary objects
class ItinerarySchema(ma.Schema):

    # validates title
    title = fields.String(
        required=True,
        validate=And(
            Length(min=5, max=50, error="Title must be between 5 and 50 characters long"),
            Regexp("^[a-zA-Z0-9 ]+$", error="Title can only contain alphanumeric characters"),
        ),
    )

    # validates content
    content = fields.String(
        required=True,
        validate=Regexp("^[a-zA-Z0-9 ]+$", error="Content can only contain alphanumeric characters"))

    # validates duration
    @validates('duration')
    def validate_duration(self, value):
        try:
            number, unit = value.split() # split input_value into number and unit
            # if unit is not in days, raise a validation error
            if unit != "day":
                raise ValidationError('Duration must be in the format "X day"')
            
            number_of_days = int(number) # convert the number to an integer
            # if the number of days is not between 1 and 30 days, raise an error
            if not 1 <= number_of_days <= 30:
                raise ValidationError("Duration must be between 1 and 30 days.")
        
        # if there's an error during split or convert, raise a validation error
        except (ValueError, IndexError): 
            raise ValidationError('Duration must be in the format "X day" where X is an integer.')

    # validates post_type
    post_type = fields.String(validate=OneOf(["Advice", "Guide"], error='Post type must be either "Advice" or "Guide"'))

    # use existing schemas for the following fields
    user = fields.Nested("UserSchema", only=["username"])
    destination = fields.Nested("DestinationSchema", only=["name", "type"])
    reviews = fields.List(fields.Nested("ReviewSchema", exclude=["itinerary"]))

    # define fields to be serialised and deserialised
    class Meta:
        fields = ("id", "title", "content", "date_posted", "duration", "post_type", "destination", "user", "reviews",)
        ordered = True  # maintain order of the fields


# create a schema instance for serialising and deserialising a single and multiple itinerary
itinerary_schema = ItinerarySchema()
itineraries_schema = ItinerarySchema(many=True, exclude=["reviews"])
