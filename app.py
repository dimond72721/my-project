from flask import Flask
from config import Config
from extensions import db, login_manager


from models import User

from auth.routes import auth
from tasks.routes import tasks


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    login_manager.init_app(app)

   
    app.register_blueprint(auth)
    app.register_blueprint(tasks)

   
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
