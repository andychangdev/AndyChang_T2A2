from flask import Blueprint, request
from init import db, bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User, user_schema, users_schema
from controllers.auth_controller import authorise_as_admin, is_user_admin


# create a blueprint for user controller
users_bp = Blueprint("users", __name__, url_prefix="/users")


# retrieve all users
@users_bp.route("/")
@jwt_required()
@authorise_as_admin
def retrieve_all_users():
    # query users table and order results by name in descending order
    stmt = db.select(User).order_by(User.date_joined.desc())
    users = db.session.scalars(stmt)
    return users_schema.dump(users)


# retrieve a user
@users_bp.route("/<int:user_id>")
def retrieve_a_user(user_id):
    # query users table 
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        return user_schema.dump(user)
    else:
        return {"Error": "User not found"}, 404
    

# update user information
@users_bp.route("/<int:user_id>", methods=["PATCH"])
@jwt_required()
def update_user_information(user_id):
    request_data = request.get_json()
    password = request_data.pop("password", None)
    # retrieve data from the request body
    data = user_schema.load(request.get_json())
    # query users table and get the user that contains the provided user_id
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # if user exists and user matches the user_id of the account, update fields
    if user:
        if str(user.id) == get_jwt_identity():
            user.username = data.get("username") or user.title
            user.email = data.get("email") or user.email

            if password:
                hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
                user.password = hashed_password

            db.session.commit()
            return user_schema.dump(user)
        else:
            return {"Error": f"Unauthorized to update user ID {user_id} information"}, 401
    else:
        return {"Error": f"User ID {user_id} not found"}, 404
    

# delete a user
@users_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    # query users table and get the user that contains the provided user_id
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # if user is admin or user_id matches the user_id of the itinerary, delete itinerary
    if is_user_admin() or str(user.id) == get_jwt_identity():
        if user:
                db.session.delete(user)
                db.session.commit()
                return {"Message": f"User ID {user_id} deleted successfully"}
        else:
            return {"Error": f"User ID {user_id} not found"}, 404
    else: 
        return {"Error": f"Unauthorized to delete User ID {user_id}"}, 401
