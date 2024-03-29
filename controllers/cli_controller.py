from datetime import date

from flask import Blueprint
from init import db, bcrypt

from models.user import User
from models.itinerary import Itinerary
from models.destination import Destination
from models.review import Review


# create a blueprint
db_commands = Blueprint("db", __name__)


# Create tables in the database
@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created successfully.")


# Drop tables from the database
@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables deleted successfully.")


# Seed the tables into the database
@db_commands.cli.command("seed")
def seed_tables():

    # seed data for users
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


    # seed data for destination
    destinations = [
        Destination(
            name="Australia",
            type="Country"
        ),
        Destination(
            name="France",
            type="Country"
        ),
        Destination(
            name="Singapore",
            type="Country"
        ),
        Destination(
            name="Brisbane",
            type="City"
        ),
        Destination(
            name="Melbourne",
            type="City"
        ),
    ]
    db.session.add_all(destinations)


    # seed data for itineraries
    itineraries = [
        Itinerary(
            title="Trip 1",
            content="The quick brown fox jumps over the lazy dog",
            date_posted=date.today(),
            duration="3 days",
            post_type="Guide",
            destination=destinations[0],
            user=users[0]
        ),
        Itinerary(
            title="Trip 2",
            content="Grumpy wizards make toxic brew for the evil Queen and Jack",
            date_posted=date.today(),
            duration="6 days",
            post_type="Guide",
            destination=destinations[0],
            user=users[1]
        ),
        Itinerary(
            title="Trip 3",
            content="The quick jogger zips past lazy walkers",
            date_posted=date.today(),
            duration="1 week",
            post_type="Advice",
            destination=destinations[1],
            user=users[1]
        ),
        Itinerary(
            title="Trip 4",
            content="Five dozen quirky elves quickly jump between hedges",
            date_posted=date.today(),
            duration="2 weeks",
            post_type="Advice",
            destination=destinations[3],
            user=users[1]
        ),
    ]
    db.session.add_all(itineraries)


    # seed data for reviews
    reviews = [
        Review(
            rating=5,
            content="The quick brown fox jumps over the lazy dog",
            date_posted=date.today(),
            user=users[0],
            itinerary=itineraries[0]
        ),
        Review(
            rating=4,
            content="Grumpy wizards make toxic brew for the evil Queen and Jack",
            date_posted=date.today(),
            user=users[1],
            itinerary=itineraries[0]
        ),
        Review(
            rating=1,
            content="The quick jogger zips past lazy walkers",
            date_posted=date.today(),
            user=users[1],
            itinerary=itineraries[1]
        ),
        Review(
            rating=2,
            content="Five dozen quirky elves quickly jump between hedges",
            date_posted=date.today(),
            user=users[1],
            itinerary=itineraries[2]
        )
    ]
    db.session.add_all(reviews)


    # commit tables into database
    db.session.commit()
    print("Tables seeded successfully.")