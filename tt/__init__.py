from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from .shop import shop_page
from datetime import datetime
from hashlib import pbkdf2_hmac

def hashp(password):
    return pbkdf2_hmac("sha256", password.encode(), b"n0t-$0-s3cur3...", 1000000)

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    has_verified_email = db.Column(db.Boolean, nullable=False, default=False)
    wants_spam = db.Column(db.Boolean, nullable=False, default=True)
    password_hash = db.Column(db.LargeBinary(32), nullable=False)
    stripe_customer = db.Column(db.Text)
    markers = db.relationship("Marker", backref="owner")
    transactions = db.relationship("TransactionInfo", backref="user")

    def __repr__(self):
        return '<User %r>' % self.email

class TransactionInfo(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    address1 = db.Column(db.Text, nullable=False)
    address2 = db.Column(db.Text)
    zip_code = db.Column(db.Text, nullable=False)
    region = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    stripe_customer = db.Column(db.Text, nullable=False)
    stripe_session = db.Column(db.Text, nullable=False)
    stripe_payment_intent = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<TransactionInfo %r>' % self.date.strftime("%Y-%m-%d %H:%M")

# A single creator per marker
# only they can add new tests to it, or change info about it
class Marker(db.Model):
    __tablename__ = "markers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    tests = db.relationship("Test", backref="marker")
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Marker %r>' % self.name

# linked to a marker
class Test(db.Model):
    __tablename__ = "tests"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    lead = db.Column(db.Float, nullable=False)
    marker_id = db.Column(db.Integer, db.ForeignKey('markers.id'), nullable=False)
    # add other testing things later on
    
    def __repr__(self):
        return '<Test %r>' % self.date.strftime("%Y-%m-%d")

app.register_blueprint(shop_page, url_prefix="/shop")

@app.route("/")
def hello_world():
    return render_template("error.html", n="Hello, World!")

@app.errorhandler(404)
def george_not_found(e):
    return render_template('error.html', n=404), 404
