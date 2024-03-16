from datetime import date

from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.itinerary import Itinerary, itineraries_schema, itinerary_schema
from models.destination import Destination


itineraries_bp = Blueprint("itineraries", __name__, url_prefix="/itineraries")


# retrieve all itineraries
@itineraries_bp.route("/")
def get_all_itineraries():
    # query itinerary table and order results by date_posted in descending order
    stmt = db.select(Itinerary).order_by(Itinerary.date_posted.desc())
    itineraries = db.session.scalars(stmt)
    return itineraries_schema.dump(itineraries)


# retrieve a specific itinerary
@itineraries_bp.route("/<int:itinerary_id>")
def get_one_itinerary(itinerary_id):
    # query itinerary table where itinerary_id matches the provided itinerary_id
    stmt = db.select(Itinerary).filter_by(id=itinerary_id)
    itinerary = db.session.scalar(stmt)
    if itinerary:
        return itinerary_schema.dump(itinerary)
    else:
        return {"Error": f"Itinerary ID {itinerary_id} not found"}, 404


# create a itinerary
@itineraries_bp.route("/", methods=["POST"])
@jwt_required()
def create_itinerary():
    # retrieve data from the request body
    data = request.get_json()

    # query destination table to get the destination_id that matches the provided destination_name
    destination_name = data.get("destination")
    selected_destination = Destination.query.filter_by(name=destination_name).first()
    if not selected_destination:
        return {"Error": "Destination not found"}, 400

    # create itinerary instance
    itinerary = Itinerary(
        title=data.get("title"),
        content=data.get("content"),
        date_posted=date.today(),
        duration=data.get("duration"),
        post_type=data.get("post_type"),
        destination=selected_destination,
        user_id=get_jwt_identity(),
    )
    # add and commit new itinerary to database
    db.session.add(itinerary)
    db.session.commit()

    # respond back to the client
    return itinerary_schema.dump(itinerary), 201


# retrieve itineraries by destination
@itineraries_bp.route("/<string:destination_name>")
def get_itineraries_by_destination(destination_name):
    # query destination table to get the destination_id that matches the provided destination_name
    destination = db.session.query(Destination).filter_by(name=destination_name).first()
    # if the destination exists, use retrieved destination_id to filter itineraries
    if destination:
        selected_destination_id = destination.id
        stmt = db.select(Itinerary).filter_by(destination_id=selected_destination_id)
        itineraries = db.session.scalars(stmt)
        return itineraries_schema.dump(itineraries)
    else:
        return {"Error": "Destination not found"}, 404
    

# update an existing itinerary
@itineraries_bp.route("/<int:itinerary_id>", methods=["PUT", "PATCH"])
def update_itinerary(itinerary_id):
    # retrieve data from the request body
    data = request.get_json()
    # query destination table to get the destination_id that matches the provided destination_name
    destination_name = data.get("destination")
    selected_destination = Destination.query.filter_by(name=destination_name).first()
    if not selected_destination:
        return {"Error": "Destination not found"}, 400
    
    stmt = db.select(Itinerary).filter_by(id=itinerary_id)
    itinerary = db.session.scalar(stmt)
    # if itinerary exists, update fields
    if itinerary:
        itinerary.title = data.get('title') or itinerary.title
        itinerary.content = data.get('content') or itinerary.content
        itinerary.duration = data.get('duration') or itinerary.duration
        itinerary.post_type = data.get('post_type') or itinerary.post_type
        itinerary.destination = selected_destination or itinerary.destination

        db.session.commit()
        return itinerary_schema.dump(itinerary)
    else:
        return {'Error': f"Itinerary ID {itinerary_id} not found"}, 404
    

# delete an existing itinerary
@itineraries_bp.route('/<int:itinerary_id>', methods=['DELETE'])
def delete_card(itinerary_id):
    # query itinerary table where itinerary_id matches the provided itinerary_id
    stmt = db.select(Itinerary).filter_by(id=itinerary_id)
    itinerary = db.session.scalar(stmt)
    if itinerary:
        db.session.delete(itinerary)
        db.session.commit()
        return {'Message': f"Itinerary titled '{itinerary.title}' deleted successfully"}
    else:
        return {"Error": f"Itinerary ID {itinerary_id} not found"}, 404

