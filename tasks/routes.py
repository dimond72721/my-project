from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models import Task

tasks = Blueprint("tasks", __name__)


@tasks.route("/")
@login_required
def index():

    task_list = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()

    return render_template("index.html", tasks=task_list)


@tasks.route("/add", methods=["POST"])
@login_required
def add_task():

    title = request.form.get("title")
    description = request.form.get("description")

    # Серверная проверка
    if not title or title.strip() == "":
        flash("Назва завдання не може бути порожньою.", "danger")
        return redirect(url_for("tasks.index"))

    task = Task(
        title=title,
        description=description,
        user_id=current_user.id
    )

    db.session.add(task)
    db.session.commit()

    flash("Завдання додано.", "success")

    return redirect(url_for("tasks.index"))


@tasks.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_task(id):

    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")

        if not title or title.strip() == "":
            flash("Назва не може бути порожньою.", "danger")
            return redirect(url_for("tasks.edit_task", id=id))

        task.title = title
        task.description = description

        db.session.commit()

        flash("Завдання оновлено.", "success")

        return redirect(url_for("tasks.index"))

    return render_template("edit.html", task=task)


@tasks.route("/delete/<int:id>")
@login_required
def delete_task(id):

    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    db.session.delete(task)
    db.session.commit()

    flash("Завдання видалено.", "warning")

    return redirect(url_for("tasks.index"))


@tasks.route("/toggle/<int:id>")
@login_required
def toggle_task(id):

    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    task.completed = not task.completed

    db.session.commit()

    return redirect(url_for("tasks.index"))
