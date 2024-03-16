from init import db, ma
from marshmallow import fields

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String)
    comment = db.Column(db.Text)
    date_posted = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey("itineraries.id"), nullable=False)

    user = db.relationship("User", back_populates="reviews")
    itinerary = db.relationship("Itinerary", back_populates="reviews")


class ReviewSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['username'])
    itinerary = fields.Nested('ItinerarySchema', exclude=['reviews'])

    class Meta:
        fields = ("id", "rating", "comment", "date_posted", "user", "itinerary")

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)