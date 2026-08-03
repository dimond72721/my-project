from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from database import (
    get_tasks,
    get_task,
    create_task,
    update_task,
    delete_task,
    toggle_task_status
)

tasks = Blueprint("tasks", __name__)


@tasks.route("/")
@login_required
def index():

    task_list = get_tasks(current_user.id)

    return render_template("index.html", tasks=task_list)


@tasks.route("/add", methods=["POST"])
@login_required
def add_task():

    title = request.form.get("title")
    description = request.form.get("description")

    if not title or title.strip() == "":
        flash("Назва завдання не може бути порожньою.", "danger")
        return redirect(url_for("tasks.index"))

    create_task(title, description, current_user.id)

    flash("Завдання додано.", "success")

    return redirect(url_for("tasks.index"))


@tasks.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_task(id):

    task = get_task(id, current_user.id)

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")

        if not title or title.strip() == "":
            flash("Назва не може бути порожньою.", "danger")
            return redirect(url_for("tasks.edit_task", id=id))

        update_task(task, title, description)

        flash("Завдання оновлено.", "success")

        return redirect(url_for("tasks.index"))

    return render_template("edit.html", task=task)


@tasks.route("/delete/<int:id>")
@login_required
def delete(id):

    task = get_task(id, current_user.id)

    delete_task(task)

    flash("Завдання видалено.", "warning")

    return redirect(url_for("tasks.index"))


@tasks.route("/toggle/<int:id>")
@login_required
def toggle(id):

    task = get_task(id, current_user.id)

    toggle_task_status(task)

    return redirect(url_for("tasks.index"))
