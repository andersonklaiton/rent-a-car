from flask import Flask
from flask_migrate import Migrate

def init_app(app: Flask):

    from app.models.address_model import Address
    from app.models.cars_model import Cars
    from app.models.rental_cars_model import RentalCars
    from app.models.state_model import States
    from app.models.users_model import Users

    Migrate(
        app,
        app.db,
        compare_types=True
    )