from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required

from models.destination import Destination, destinations_schema, destination_schema
from controllers.auth_controller import authorise_as_admin


# create a blueprint for destination controller
destinations_bp = Blueprint("destinations", __name__, url_prefix="/destinations")


# create a destination
@destinations_bp.route("/", methods=["POST"])
@jwt_required()
@authorise_as_admin
def create_destinations():
    data = destination_schema.load(request.get_json())
    destination_name = Destination.query.filter_by(name=data.get("name")).first()
    if destination_name:
        return {"Error": "Destination name already exists"}, 409

    # create destination instance
    destination = Destination(
        name=data.get("name"),
        type=data.get("type"),
    )
    # add and commit new itinerary to database
    db.session.add(destination)
    db.session.commit()

    # respond back to the client
    return destination_schema.dump(destination), 201
    

# retrieve all destinations
@destinations_bp.route("/")
def get_all_destinations():
    # query destinations table and order results by name in ascending order
    stmt = db.select(Destination).order_by(Destination.name.asc())
    destinations = db.session.scalars(stmt)
    return destinations_schema.dump(destinations)


# retrieve all destinations by type
@destinations_bp.route("/<string:destination_type>")
def get_destinations_by_type(destination_type):
    destination_type = destination_type.capitalize()
    # query destination table and get the destinations that contains the provided destination_type
    stmt = db.session.query(Destination).filter_by(type=destination_type)
    # if destinations with that type exists, retrieve itineraries that contain the destination
    destinations = db.session.scalars(stmt).all()

    if destinations:
        return destinations_schema.dump(destinations)
    else:
        return {"Error": "Destination type not found"}, 404
    

# delete an existing destination
@destinations_bp.route("/<string:destination_name>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_destination(destination_name):
    destination_name = destination_name.capitalize()
    # query destination table and get the destination that contains the provided destination_name
    stmt = db.select(Destination).filter_by(name=destination_name)
    destination = db.session.scalar(stmt)
    # if destination exists, delete destination
    if destination:
            db.session.delete(destination)
            db.session.commit()
            return {"Message": f'Destination "{destination_name}" deleted successfully'}
    else:
        return {"Error": f'Destiation "{destination_name}" not found'}, 404


