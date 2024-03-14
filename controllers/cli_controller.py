from datetime import date

from flask import Blueprint
from init import db, bcrypt
from models.user import User

db_commands = Blueprint("db", __name__)

# Create the tables in the database
@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created successfully.")

# Drops all tables from the database
@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables deleted successfully.")

# Seed the tables in the database
@db_commands.cli.command("seed")
def seed_tables():
    users = [
        User(
            username="Admin",
            email="admin@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8"),
            date_joined=date.today(),
            is_admin=True
        ),
        User(
            username="User 1",
            email="user1@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8"),
            date_joined=date.today(),
        )
    ]

    db.session.add_all(users)
    db.session.commit()
    print("Tables seeded successfully.")