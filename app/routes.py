from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from calendar import monthrange
from datetime import datetime
from app.extensions import db, migrate
from app.models import User, Habit, HabitStatus
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


# The routing for dashboard
@main.route("/dashboard")
@login_required
def dashboard():
    current_date = datetime.today()
    current_month = current_date.strftime('%B')
    current_month_num = current_date.month
    current_year = current_date.year
    days_in_month = monthrange(current_year, current_month_num)[1]
    start_day = current_date.replace(day=1).weekday()

    #! Example Habits for testing (replace with DB queries).
    habits = [
        {"id": 1, "name": "Journal", "is_completed": lambda day: day % 2 == 0},
        {"id": 2, "name": "Exercise", "is_completed": lambda day: day % 3 == 0},
    ]

    return render_template(
        "dashboard.html",
        current_month=current_month,
        current_month_num=current_month_num,
        current_year=current_year,
        days_in_month=days_in_month,
        start_day=start_day,
        habits=habits
    )


# The routing to add habits.
@main.route("/add_habit", methods=["POST"])
@login_required
def add_habit():
    # Get the habit name from the form
    habit_name = request.form.get("habit_name")

    if habit_name:
        # Add the habit to the database
        new_habit = Habit(name=habit_name, user_id=current_user.id)
        db.session.add(new_habit)
        db.session.commit()
        flash("Habit added successfully!", "success")
    else:
        flash("Habit name cannot be empty", "danger")

    # Redirect back to the dashboard
    return redirect(url_for("main.dashboard"))


@main.route("/toggle_habit/<int:habit_id>/<habit_date>", methods=["POST"])
@login_required
def toggle_habit(habit_id, habit_date):
    habit = Habit.query.get_or_404(habit_id)
    habit_date = datetime.strptime(habit_date, "%Y-%m-%d").date()

    # Check if there's already a status for this habit and date
    status = HabitStatus.query.filter_by(
        habit_id=habit.id, date=habit_date).first()

    if status:
        # Toggle the completion status
        status.completed = not status.completed
    else:
        # Create a new status
        new_status = HabitStatus(
            habit_id=habit.id, date=habit_date, completed=True)
        db.session.add(new_status)

    db.session.commit()
    return redirect(url_for("main.dashboard"))
