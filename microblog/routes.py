from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from microblog import app, db
from microblog.forms import LoginForm, RegistrationForm
from microblog.models import User, Post


@app.route("/")
@login_required
def index_page():
    posts = Post.query.all()  # Get all the posts from the database
    return render_template("index.html", title="Home")


@app.route("/register", methods=["GET", "POST"])
def register_page():
    # Redirect the user to homepage if they are already logged in
    if current_user.is_authenticated:
        return redirect(url_for("index_page"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for("login_page"))

    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    """Logs the user in if credentials are valid, else redirects
       user back to the login page.
    """
    # Redirect the user to homepage if they are already logged in
    if current_user.is_authenticated:
        return redirect(url_for("index_page"))

    form = LoginForm()
    if form.validate_on_submit():
        # Get the user's username from the database
        user = User.query.filter_by(username=form.username.data).first()
        # Redirect user if details are not valid
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Username or Password!!")
            return redirect(url_for("login_page"))
        # Login the user if details is valid
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if next_page:
            return redirect(next_page)
        return redirect(url_for("index_page"))

    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    """Logs the user out of all sessions."""
    logout_user()
    return redirect(url_for("index_page"))
