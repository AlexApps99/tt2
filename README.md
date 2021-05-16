Password hashing = hashlib

Use blueprints to split up code nicely
https://flask.palletsprojects.com/en/2.0.x/blueprints/

https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/

make blog last

Offload as much work as possible
Eg stripe does carbon offsetting, email receipts
I may want to make a custom transaction form, but that's easy

Support localization early on
Jinja supports either Babel or Python's builtin gettext
Since I only have one other language I could probably also
Just make my own extension and have something like `lang("Welcome", "Kia ora")` where it picks for me

# looks a bit chonky but maybe maybe
https://flask-security-too.readthedocs.io/en/stable/
https://pythonhosted.org/Flask-Principal/

Consider using OAuth to log in
Eg google account
