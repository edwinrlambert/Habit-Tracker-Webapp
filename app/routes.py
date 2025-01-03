from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, migrate
from app.models import User
from app.forms import RegistrationForm, LoginForm

# Define the Blueprint
main = Blueprint("main", __name__)


# The default routing.
@main.route("/")
def index():
    # Check if the user is authenticated
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    else:
        return redirect(url_for("main.login"))


# The routing for dashboard
@main.route("/dashboard")
@login_required
def dashboard():
    return "Welcome to the Habit Tracker Webapp!"


# The routing for registration.
@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method="pbkdf2:sha256")
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please Log in.", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)


# The routing for login.
@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid email or password.", "danger")
    return render_template("login.html", form=form)


# The routing for logout.
@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.login"))
