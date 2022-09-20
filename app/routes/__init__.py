from flask import Blueprint, Flask
from app.routes.users_route import bp as bp_users
from app.routes.category_route import bp as bp_category
from app.routes.cars_route import bp as bp_cars
from app.routes.address_route import bp as bp_address
from app.routes.maintenance_route import bp as bp_maintenance
from app.routes.rental_cars_route import bp as bp_rentals

bp_api = Blueprint('api', __name__)

def init_app(app: Flask):

    bp_api.register_blueprint(bp_users)
    bp_api.register_blueprint(bp_cars)
    bp_api.register_blueprint(bp_category)
    bp_api.register_blueprint(bp_address)
    bp_api.register_blueprint(bp_maintenance)
    bp_api.register_blueprint(bp_rentals)
    from app.routes.mail_route import bp as bp_mail
    bp_api.register_blueprint(bp_mail)

    app.register_blueprint(bp_api) 