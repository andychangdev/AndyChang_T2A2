from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.itinerary import Itinerary, itineraries_schema, itinerary_schema
from models.country import Country


itineraries_bp = Blueprint("itineraries", __name__, url_prefix="/itineraries")


# retrieve all itineraries
@itineraries_bp.route("/")
def get_all_itineraries():
    stmt = db.select(Itinerary).order_by(Itinerary.date_posted.desc())
    itineraries = db.session.scalars(stmt)
    return itineraries_schema.dump(itineraries)


# retrieve a specific itinerary
@itineraries_bp.route("/<int:itinerary_id>")
def get_one_itinerary(itinerary_id):
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

    # query the country table to get the country_id based on country_name
    country_name = data.get("country")
    selected_country = Country.query.filter_by(name=country_name).first()
    # if the country does not exist, return an error message
    if not selected_country:
        return {"Error": "Country not found"}

    # create a new itinerary instance
    itinerary = Itinerary(
        title=data.get("title"),
        content=data.get("content"),
        date_posted=date.today(),
        duration=data.get("duration"),
        post_type=data.get("post_type"),
        country=selected_country,
        user_id=get_jwt_identity(),
    )
    # add and commit new itinerary to database
    db.session.add(itinerary)
    db.session.commit()

    # respond back to the client
    return itinerary_schema.dump(itinerary), 201


# retrieve itineraries by country
@itineraries_bp.route("/<string:country_name>")
def get_itineraries_by_country(country_name):
    # query the country table to get the country_id based on country_name
    country = db.session.query(Country).filter_by(name=country_name).first()
    # if the country exists, retrieve its country_id
    if country:
        selected_country_id = country.id

        # use the country_id to filter itineraries
        stmt = db.select(Itinerary).filter_by(country_id=selected_country_id)
        itineraries = db.session.scalars(stmt)
        return itineraries_schema.dump(itineraries)
    else:
        # else country does not exist, return an error message
        return {"Error": "Country not found"}, 404
    
# delete an existing itinerary
@itineraries_bp.route('/<int:itinerary_id>', methods=['DELETE'])
def delete_card(itinerary_id):
    stmt = db.select(Itinerary).filter_by(id=itinerary_id)
    itinerary = db.session.scalar(stmt)
    if itinerary:
        db.session.delete(itinerary)
        db.session.commit()
        return {'Message': f"Itinerary titled '{itinerary.title}' deleted successfully"}
    else:
        return {"Error": f"Itinerary ID {itinerary_id} not found"}, 404


# update an existing itinerary
@itineraries_bp.route("/<int:itinerary_id>", methods=["PUT", "PATCH"])
def update_itinerary(itinerary_id):
    # retrieve request body
    data = request.get_json()

    # query the country table to get the country_id based on country_name
    country_name = data.get("country")
    selected_country = Country.query.filter_by(name=country_name).first()
    # if the country does not exist, return an error message
    if not selected_country:
        return {"Error": "Country not found"}
    
    stmt = db.select(Itinerary).filter_by(id=itinerary_id)
    itinerary = db.session.scalar(stmt)
    # if itinerary exists
    if itinerary:
        # update fields
        itinerary.title = data.get('title') or itinerary.title
        itinerary.content = data.get('content') or itinerary.content
        itinerary.duration = data.get('duration') or itinerary.duration
        itinerary.post_type = data.get('post_type') or itinerary.post_type
        itinerary.country = selected_country or itinerary.country

        # commit changes to database
        db.session.commit()
        # return the 
        return itinerary_schema.dump(itinerary)
    # else if itinerary does not exist, return an error message
    else:
        return {'Error': f"Itinerary ID {itinerary_id} not found"}, 404

