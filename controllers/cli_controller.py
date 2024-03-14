from datetime import date

from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.itinerary import Itinerary

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

    itineraries = [
        Itinerary(
            title="Trip 1",
            content="Trip 1 content",
            date=date.today(),
            duration="7 days",
            type="Guide",
            user=users[0]
        ),
        Itinerary(
            title="Trip 2",
            content="Trip 2 content",
            date=date.today(),
            duration="6 days",
            type="Guide",
            user=users[0]
        ),
        Itinerary(
            title="Trip 3",
            content="Trip 3 content",
            date=date.today(),
            duration="4 days",
            type="Advice",
            user=users[1]
        ),
        Itinerary(
            title="Trip 4",
            content="Trip 4 content",
            date=date.today(),
            duration="2 days",
            type="Advice",
            user=users[1]
        ),
    ]

    db.session.add_all(itineraries)
    
    db.session.commit()
    print("Tables seeded successfully.")