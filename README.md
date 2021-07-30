Password hashing = hashlib
https://www.health.govt.nz/system/files/documents/publications/dwsnz-2005-revised-mar2019.pdf

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


geolocation api to get location?
`const getCurrentPosition=o=>{return new Promise((resolve,reject)=>navigator.geolocation.getCurrentPosition(p=>resolve(p),e=>reject(e),o))};getCurrentPosition({enableHighAccuracy:!0,timeout:1000}).then(p=>console.log(p.coords))`

have all the login stuff, sadly
I will need to do emails out and subscriptions?
so i might as well track submitted tests and other stuff


index
- branding
- talk about how great we are
- shop
- map
- blog
- help/faq
- about us (press (sh/k)it)
- about our product
- privacy policy, ToS

shop
- subdomain
- NOT storbie because its shit
- refund, shipping policy
- credit card (probably stripe)
- bank deposit
- https://support.nzpost.co.nz/app/answers/detail/a_id/1469/~/new-zealand-post%E2%80%99s-addressing-api (FREE)

blog
- subdomain, maybe just jekyll or wordpress or something
- maybe just do a mailing list if i can't be arsed

map
- 


https://github.com/Leaflet/Leaflet.toolbar
for a plus button
