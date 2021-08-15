from flask import Flask
from tt.db import db, User, hashp
from tt import create_app

def setup_db(app):
    with app.app_context():
        #db.create_all()
        me = User(email=input("Email: "),
                password_hash=hashp(input("Password: ")),
                godmode=bool(input("Godmode: ")))
        db.session.add(me)
        db.session.commit()

def main():
    app = create_app()
    setup_db(app)

if __name__ == "__main__":
    main()

