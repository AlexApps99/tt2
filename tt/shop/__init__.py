from flask import Blueprint, render_template

shop_page = Blueprint("shop", __name__, template_folder="templates")

@shop_page.route('/')
def show():
    return render_template("error.html", n="Wii Shop Channel")
