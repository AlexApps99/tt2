from flask import Blueprint, render_template, jsonify, redirect
from wtforms import StringField, DecimalField, TextAreaField, IntegerField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, InputRequired, Length, Email, NumberRange
from ..db import Marker, db, Test
from datetime import datetime
from flask_login import current_user

map_page = Blueprint("map", __name__, template_folder="templates")


class UploadForm(FlaskForm):
    lat = DecimalField('lat', validators=[DataRequired()])
    lon = DecimalField('lon', validators=[DataRequired()])
    markerTitle = StringField('markerTitle',
                              validators=[DataRequired(),
                                          Length(5, 50)])
    markerDesc = TextAreaField('markerDesc',
                               validators=[Length(0,
                                                  50)])  # make not compulsory
    nitrate = DecimalField('nitrate',
                           validators=[InputRequired(),
                                       NumberRange(0, 50)])
    nitride = DecimalField('nitride',
                           validators=[InputRequired(),
                                       NumberRange(0, 10)])
    ph = IntegerField('ph', validators=[DataRequired(), NumberRange(4, 10)])
    free_cl = DecimalField('free_cl',
                           validators=[InputRequired(),
                                       NumberRange(0, 10)])
    total_cl = DecimalField('total_cl',
                            validators=[InputRequired(),
                                        NumberRange(0, 10)])
    hardness = IntegerField('hardness',
                            validators=[InputRequired(),
                                        NumberRange(0, 400)])
    #marker_id = StringField('marker_id')


# Use anchors to hone in on specific markers
# clientside
@map_page.route('/', methods=['GET', 'POST'])
def show():
    form = UploadForm()
    if current_user.is_authenticated and form.validate_on_submit():
        marker = Marker(name=form.markerTitle.data,
                        description=form.markerDesc.data,
                        lat=form.lat.data,
                        lon=form.lon.data)
        test = Test(
            date=datetime.now(),
            nitrate=form.nitrate.data,
            nitride=form.nitride.data,
            ph=form.ph.data,
            free_cl=form.free_cl.data,
            total_cl=form.total_cl.data,
            hardness=form.hardness.data,
        )
        # lol i need to sort out accounts ASAP
        #marker.owner = me
        test.marker = marker
        marker.owner = current_user
        db.session.add(marker)
        #db.session.add(me)
        db.session.commit()
    else:
        print(form.errors)
    return render_template("map.html", form=form)


@map_page.route('/map.json')
def map_data():
    return jsonify([[m.id, [m.lat, m.lon],
                     min(quality(m.tests[-1]))] for m in Marker.query.all()])


def gen_test_obj(t):
    q = quality(t)
    return {
        "date": str(t.date),
        "quality": min(q),
        "qualities": q,
        "nitrate": t.nitrate,
        "nitride": t.nitride,
        "ph": t.ph,
        "free_cl": t.free_cl,
        "total_cl": t.total_cl,
        "hardness": t.hardness
    }


def quality(t):
    q = []
    if t.nitrate < 1:
        q.append(3)
    elif t.nitrate < 2:
        q.append(2)
    else:
        q.append(1)

    if t.nitride < 1:
        q.append(3)
    elif t.nitride < 2:
        q.append(2)
    else:
        q.append(1)

    if t.ph == 7:
        q.append(3)
    elif t.ph == 6 or t.ph == 8:
        q.append(2)
    else:
        q.append(1)

    if t.free_cl < 1:
        q.append(3)
    elif t.free_cl < 2:
        q.append(2)
    else:
        q.append(1)

    if t.total_cl < 1:
        q.append(3)
    elif t.total_cl < 2:
        q.append(2)
    else:
        q.append(1)

    if t.hardness < 1:
        q.append(3)
    elif t.hardness < 2:
        q.append(2)
    else:
        q.append(1)

    return q


@map_page.route('/<int:n>.json')
def marker_data(n):
    marker = Marker.query.get(n)
    if marker is None:
        return jsonify(None), 404
    return {
        "id":
        marker.id,
        "name":
        marker.name,
        "description":
        marker.description,
        "pos": [marker.lat, marker.lon],
        "tests": [
            a[1]
            for a in sorted([(t.date, gen_test_obj(t)) for t in marker.tests],
                            key=lambda x: x[0],
                            reverse=True)
        ],
        "owned":
        False,  # TODO
    }
