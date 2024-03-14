from init import db, ma


# create database that represents the user entity
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_joined = db.Column(db.Date, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


# creates a schema for user object
class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "username", "email", "password", "date_joined", "is_admin")


user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])
