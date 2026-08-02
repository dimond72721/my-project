from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from extensions import db
from models import User

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not username or not email or not password:
            flash("Заповніть усі поля.", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Користувач вже існує.", "warning")
            return redirect(url_for("auth.register"))

        user = User(
            username=username,
            email=email
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Реєстрація успішна. Тепер увійдіть.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):

            login_user(user)

            flash("Вхід виконано.", "success")

            return redirect(url_for("tasks.index"))

        flash("Невірний email або пароль.", "danger")

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Ви вийшли з акаунта.", "info")

    return redirect(url_for("auth.login"))
