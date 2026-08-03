from extensions import db
from models import Task


def get_tasks(user_id):
    return (
        Task.query
        .filter_by(user_id=user_id)
        .order_by(Task.created_at.desc())
        .all()
    )


def get_task(task_id, user_id):
    return Task.query.filter_by(
        id=task_id,
        user_id=user_id
    ).first_or_404()


def create_task(title, description, user_id):
    task = Task(
        title=title,
        description=description,
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()


def update_task(task, title, description):
    task.title = title
    task.description = description

    db.session.commit()


def delete_task(task):
    db.session.delete(task)
    db.session.commit()


def toggle_task_status(task):
    task.completed = not task.completed

    db.session.commit()
