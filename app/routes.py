from flask import Blueprint, render_template

# Define the Blueprint
main = Blueprint("main", __name__)


# Define a basic routing for testing
@main.route("/")
def index():
    return "Welcome to the Habit Tracker Webapp!"
