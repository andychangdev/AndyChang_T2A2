from datetime import date

from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.itinerary import Itinerary, itineraries_schema, itinerary_schema
from models.destination import Destination
from controllers.auth_controller import is_user_admin
from controllers.review_controller import reviews_bp


itineraries_bp = Blueprint("itineraries", __name__, url_prefix="/itineraries")
itineraries_bp.register_blueprint(reviews_bp)


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
    # query itinerary table and get the itinerary that contains the provided itinerary_id
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
    data = itinerary_schema.load(request.get_json())
    destination_name = data["destination"]["name"]
    # retrieve data of destination
    provided_destination = db.session.query(Destination).filter_by(name=destination_name).first()
    # If the destination does not exist
    if not provided_destination:
        return {"error": f"Destination '{destination_name}' not found"}, 404

    # create itinerary instance
    itinerary = Itinerary(
        title=data.get("title"),
        content=data.get("content"),
        date_posted=date.today(),
        duration=data.get("duration"),
        post_type=data.get("post_type"),
        destination=provided_destination,
        user_id=get_jwt_identity(),
    )
    # add and commit new itinerary to database
    db.session.add(itinerary)
    db.session.commit()

    # respond back to the client
    return itinerary_schema.dump(itinerary), 201


# retrieve itineraries by destination_name
@itineraries_bp.route("/<string:destination_name>")
def get_itineraries_by_destination_name(destination_name):
    try:
        destination_name = destination_name.capitalize()
        stmt = db.select(Itinerary).filter_by(destination_name=destination_name)
        itineraries = db.session.scalars(stmt)
        return itineraries_schema.dump(itineraries)
    except:
        return {"Error": "Destination not found"}, 404
    

# retrieve itineraries by destination_type
@itineraries_bp.route("/type/<string:destination_type>")
def get_itineraries_by_destination_type(destination_type):
    try:
        destination_type = destination_type.capitalize()
        # query destination table and get the destinations that contains the provided destination_type
        destinations = db.session.query(Destination).filter_by(type=destination_type).first()
        # if destinations with that type exists, retrieve itineraries that contain the destination
        if destinations:
            selected_destination_name = destinations.name
            stmt = db.select(Itinerary).filter_by(destination_name=selected_destination_name)
            itineraries = db.session.scalars(stmt)
            return itineraries_schema.dump(itineraries)
        else:
            return {"Error": "No Destination type found"}, 404
    except:
        return {"Error": "Destination type not found"}, 404
    

# update an existing itinerary
@itineraries_bp.route("/<int:itinerary_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_itinerary(itinerary_id):
    # retrieve data from the request body
    data = itinerary_schema.load(request.get_json())
    destination_name = data["destination"]["name"]
    # retrieve data of destination
    provided_destination = db.session.query(Destination).filter_by(name=destination_name).first()
    # If the destination does not exist
    if not provided_destination:
        return {"error": f"Destination '{destination_name}' not found"}, 404
    
    # query itinerary table and get the itinerary that contains the provided itinerary_id
    stmt = db.select(Itinerary).filter_by(id=itinerary_id)
    itinerary = db.session.scalar(stmt)
    # if user_id matches the user_id of the itinerary
    if str(itinerary.user.id) == get_jwt_identity():
    # if itinerary exists, update fields
        if itinerary:
            itinerary.title = data.get("title") or itinerary.title
            itinerary.content = data.get("content") or itinerary.content
            itinerary.duration = data.get("duration") or itinerary.duration
            itinerary.post_type = data.get("post_type") or itinerary.post_type
            itinerary.destination = provided_destination or itinerary.destination

            db.session.commit()
            return itinerary_schema.dump(itinerary)
        else:
            return {"Error": f"Itinerary ID {itinerary_id} not found"}, 404
    else:
        return {"Error": f"Unauthorized to delete itinerary ID {itinerary_id}"}, 401
    

# delete an existing itinerary
@itineraries_bp.route("/<int:itinerary_id>", methods=["DELETE"])
@jwt_required()
def delete_card(itinerary_id):
    # query itinerary table and get the itinerary that contains the provided itinerary_id
    stmt = db.select(Itinerary).filter_by(id=itinerary_id)
    itinerary = db.session.scalar(stmt)
    # if user is admin or user_id matches the user_id of the itinerary
    is_admin = is_user_admin()
    if is_admin or str(itinerary.user.id) == get_jwt_identity():
        if itinerary:
                db.session.delete(itinerary)
                db.session.commit()
                return {"Message": f"Itinerary ID {itinerary_id} deleted successfully"}
        else:
            return {"Error": f"Itinerary ID {itinerary_id} not found"}, 404
    else: 
        return {"Error": f"Unauthorized to delete itinerary ID {itinerary_id}"}, 401