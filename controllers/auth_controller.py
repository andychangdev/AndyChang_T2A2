from datetime import date, timedelta

from flask import Blueprint, request
from init import db, bcrypt
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity

from models.user import User, user_schema


# create a blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# register a user
@auth_bp.route("/register", methods=["POST"])
def auth_register():
    try:
        # retrieve data from the request body and remove password
        request_data = request.get_json()
        password = request_data.pop("password", None)
        # retrieve data from the request body
        data = user_schema.load(request_data)
        # create user instance
        user = User(
            username=data.get("username"),
            email=data.get("email"),
            date_joined=date.today()
        )
        # if password exists, then hash the password
        if password:
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            user.password = hashed_password
        # add and commit the user to database
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201
    
    
    except IntegrityError as error:
        # if error is due to empty data field, return error message
        if error.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"Error": f"{error.orig.diag.column_name} field missing."}, 409
        # if error is due to duplicate data, return error message
        if error.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            constraint_name = error.orig.diag.constraint_name
            if "username" in constraint_name:
                return {"Error": f"Username already taken."}, 409
            elif "email" in constraint_name:
                return {"Error": f"Email address already registered."}, 409


# login an existing user
@auth_bp.route("/login", methods=["POST"])
def auth_login():
    # retrieve data from the request body and remove password
    request_data = request.get_json()
    password = request_data.pop("password", None)
    # retrieve data from the request body
    data = user_schema.load(request_data)
    # retrieve the user with email address
    stmt = db.select(User).filter_by(email=data.get("email"))
    user = db.session.scalar(stmt)
    # if user exists and password is correct, create jwt token and return user info along with token
    if user:
        if bcrypt.check_password_hash(user.password, password):
            token = create_access_token(
                identity=str(user.id), expires_delta=timedelta(days=1)
            )
            return {"email": user.email, "token": token, "is_admin": user.is_admin}
        # else password is incorrect, return an error message
        else:
            return {"Error": "Invalid password."}, 401
    # else user does not exists, return error message
    else:
        return {"Error": "Email address not found."}, 404

# create function that checks if user is admin    
def is_user_admin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin