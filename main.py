import os
from flask import Flask
from init import db, ma, bcrypt, jwt
from marshmallow.exceptions import ValidationError


# create flask application
def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False

    # configuration settings for application
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    # connect libraries with flask app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    
    # global error handlers that catch specific error codes
    @app.errorhandler(400)
    def bad_request(error):
        return {"Error": str(error)}, 400

    @app.errorhandler(404)
    def not_found(error):
        return {"Error": str(error)}, 404

    @app.errorhandler(ValidationError)
    def validation_error(error):
        return {"error": error.messages}, 400


    # import and register blueprints for application
    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)

    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from controllers.itinerary_controller import itineraries_bp
    app.register_blueprint(itineraries_bp)

    from controllers.destination_controller import destinations_bp
    app.register_blueprint(destinations_bp)

    return app
