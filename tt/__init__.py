from flask import Flask
from datetime import datetime, timedelta

from .db import db, login_manager, User, Marker, Test, hashp
from .map import map_page
from .index import idx_page


def create_app():
    app = Flask(__name__, static_url_path='')
    app.secret_key = b'}\xdc\x04\x9e\xba\xa8\xda0,@\x8e\x03\x9a[\xec\xb9'
    if app.env == "production":
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tt.db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    login_manager.init_app(app)
    db.init_app(app)
    app.register_blueprint(map_page, url_prefix="/map")
    app.register_blueprint(idx_page)
    #app.context_processor(i18n_processor)
    if app.env != "production":
        setup_db(app)
    return app


# please consider maori it will up our grade a shitton
def i18n_processor():
    def i18n(s):
        return s

    return {"i18n": i18n, "_": i18n}


def setup_db(app):
    with app.app_context():
        db.create_all()
        me = User(email="alex.apps99@gmail.com",
                  password_hash=hashp("GeffIsGreat123"),
                  godmode=True)
        if app.env != "production":
            marker = Marker(name="Northcote College",
                            description="Testing Time HQ",
                            lat=-36.8095,
                            lon=174.7338)
            # make the current date be the default
            test = Test(
                date=datetime.now(),
                nitrate=0,
                nitrite=0,
                ph=6,
                free_cl=0,
                total_cl=0,
                hardness=0,
            )
            prevtest = Test(
                date=datetime.now() - timedelta(days=3),
                nitrate=0,
                nitrite=0,
                ph=4,
                free_cl=0,
                total_cl=0,
                hardness=0,
            )

            marker.owner = me
            prevtest.marker = marker
            test.marker = marker
        db.session.add(me)
        db.session.commit()
        # print(
        #     User.query.filter_by(username="AlexApps99")
        #         .first().markers[0].tests[0].marker.owner
        # )

def main():
    app = create_app()
    app.run()

if __name__ == "__main__":
    main()

