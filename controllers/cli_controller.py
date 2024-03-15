from datetime import date

from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.itinerary import Itinerary
from models.country import Country

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

# Seed the tables into the database
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


    countries = [
        Country(
            name="Australia"
        ),
        Country(
            name="France"
        ),
        Country(
            name="Singapore"
        ),
        Country(
            name="China"
        ),
        Country(
            name="United States of America"
        ),
    ]

    db.session.add_all(countries)

    itineraries = [
        Itinerary(
            title="Trip 1",
            content="The quick brown fox jumps over the lazy dog",
            date_posted=date.today(),
            duration="3 days",
            post_type="Guide",
            country=countries[0],
            user=users[0]
        ),
        Itinerary(
            title="Trip 2",
            content="Grumpy wizards make toxic brew for the evil Queen and Jack",
            date_posted=date.today(),
            duration="6 days",
            post_type="Guide",
            country=countries[0],
            user=users[1]
        ),
        Itinerary(
            title="Trip 3",
            content="The quick jogger zips past lazy walkers",
            date_posted=date.today(),
            duration="1 week",
            post_type="Advice",
            country=countries[1],
            user=users[1]
        ),
        Itinerary(
            title="Trip 4",
            content="Five dozen quirky elves quickly jump between hedges",
            date_posted=date.today(),
            duration="2 weeks",
            post_type="Advice",
            country=countries[2],
            user=users[1]
        ),
    ]

    db.session.add_all(itineraries)
    
    db.session.commit()
    print("Tables seeded successfully.")