from flask import render_template, url_for, redirect, flash

from microblog import app
from microblog.forms import LoginForm


@app.route("/")
def index_page():
    return render_template("index.html", name="Sparrow", title="Home")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Login requested for {form.username.data}, \
              remember_me={form.remember_me.data}")
        return redirect(url_for("index_page"))
    return render_template("login.html", title="Sign In", form=form)

