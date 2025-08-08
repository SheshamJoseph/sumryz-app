from .forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from flask import redirect, render_template, url_for, flash
from . import auth
from ..models import User
from flask_login import login_user, logout_user, login_required
from .. import db
from .utils import send_password_reset_email, verify_reset_token


@auth.route("/signup", methods=["GET", "POST"])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(
                fname = form.fname.data,
                lname = form.lname.data,
                email = form.email.data,
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful!", "success")
            
            # Possible account creation confirmation
            
            return redirect(url_for("auth.login"))
        except:
            flash("Error creating account")
    return render_template("auth/sign_up.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    # render login page here
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.check_password(form.password.data):
                login_user(user, form.remember.data)
                flash("Logged in Successfully")
                return redirect(url_for("home"))
        except:
            pass
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for("login"))


@auth.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash("Password reset email sent.", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Email not found.", "danger")
    form = ForgotPasswordForm()
    return render_template("auth/forgot_password.html", form=form)


@auth.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash("Invalid or expired token.", "danger")
        return redirect(url_for("auth.forgot_password"))

    # If the token is valid, allow the user to reset their password
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(form.password.data)
            db.session.commit()
            flash("Your password has been updated!", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("User not found.", "danger")
    
    return render_template("auth/reset_password.html", form=form)
