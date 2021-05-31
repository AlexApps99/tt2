from flask import Flask
from datetime import datetime

from .db import db, login_manager, User, Marker, Test, hashp
from .map import map_page
from .index import idx_page


def create_app():
    app = Flask(__name__, static_url_path='')
    app.secret_key = b'}\xdc\x04\x9e\xba\xa8\xda0,@\x8e\x03\x9a[\xec\xb9'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    login_manager.init_app(app)
    db.init_app(app)
    app.register_blueprint(map_page, url_prefix="/map")
    app.register_blueprint(idx_page)
    setup_db(app)
    return app


def setup_db(app):
    with app.app_context():
        db.create_all()
        me = User(
            username="AlexApps99",
            email="alex.apps99@gmail.com",
            has_verified_email=True,
            password_hash=hashp("GeffIsGreat123")
        )
        marker = Marker(
            name="Northcote College",
            description="Testing Time HQ",
            lat=-36.8095,
            lon=174.7338
        )
        # make the current date be the default
        test = Test(date=datetime.now(), nitrate=0)
        marker.owner = me
        test.marker = marker
        db.session.add(me)
        db.session.commit()
        # print(
        #     User.query.filter_by(username="AlexApps99")
        #         .first().markers[0].tests[0].marker.owner
        # )


if __name__ == "__main__":
    app = create_app()
    app.run()
