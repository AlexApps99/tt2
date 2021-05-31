from flask import Blueprint, render_template, jsonify
from ..db import Marker

map_page = Blueprint("map", __name__, template_folder="templates")


@map_page.route('/')
def show():
    return render_template("main.html", title="Mapman")


@map_page.route('/map.json')
def map_data():
    return jsonify([[m.id, [m.lat, m.lon]] for m in Marker.query.all()])


def gen_test_obj(t):
    return {
        "nitrate": t.nitrate,
        # "nitride": t.nitride,
        # "ph": t.ph,
        # "free_cl": t.free_cl,
        # "total_cl": t.total_cl,
        # "hardness": t.hardness
    }


@map_page.route('/<int:n>.json')
def marker_data(n):
    marker = Marker.query.get(n)
    if marker is None:
        return jsonify(None), 404
    return {
        "id": marker.id,
        "name": marker.name,
        "description": marker.description,
        "pos": [marker.lat, marker.lon],
        "tests": [gen_test_obj(t) for t in marker.tests],
        "owner": marker.owner.username,
    }
