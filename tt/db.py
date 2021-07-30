from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from hashlib import pbkdf2_hmac
from numpy import base_repr

db = SQLAlchemy()
login_manager = LoginManager()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    #has_verified_email = db.Column(db.Boolean, nullable=False, default=False)
    #wants_spam = db.Column(db.Boolean, nullable=False, default=True)
    godmode = db.Column(db.Boolean, nullable=False, default=False)
    password_hash = db.Column(db.LargeBinary(32), nullable=False)
    markers = db.relationship("Marker", backref="owner", cascade="all, delete-orphan")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.email


# A single creator per marker
# only they can add new tests to it, or change info about it
class Marker(db.Model):
    __tablename__ = "markers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    tests = db.relationship("Test", backref="marker", cascade="all, delete-orphan")
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Marker %r>' % self.name


# linked to a marker
class Test(db.Model):
    __tablename__ = "tests"
    # This ID directly corresponds to what we provide with each "swab"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    nitrate = db.Column(db.Float, nullable=False)
    nitrite = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=False)
    free_cl = db.Column(db.Float, nullable=False)
    total_cl = db.Column(db.Float, nullable=False)
    hardness = db.Column(db.Float, nullable=False)
    marker_id = db.Column(db.Integer,
                          db.ForeignKey('markers.id'),
                          nullable=False)

    def __repr__(self):
        return '<Test %r>' % self.date.strftime("%Y-%m-%d")


def hashp(password: str):
    return pbkdf2_hmac("sha256", password.encode(),
                       b'zA\xee\xdbk\xd5\xc1@\xa8\xee\x83\xfft\x9d\x9c\xa0',
                       1000000)


def decode_test_id(test_id: str):
    return int(test_id, 36)


def encode_test_id(n: int):
    return base_repr(n, base=36)


@login_manager.user_loader
def load_user(user_id: str):
    if not isinstance(user_id, int):
        try:
            i = int(user_id)
        except ValueError:
            return None
    else:
        i = user_id
    return User.query.get(i)


def get_user(email: str, password: str):
    u = User.query.filter_by(email=email).first()
    if u is not None and u.password_hash == hashp(password):
        return u
    else:
        return None
