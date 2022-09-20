from flask import Blueprint

from app.controllers import cars_controller

bp = Blueprint("cars", __name__, url_prefix="/cars")

bp.post("")(cars_controller.create_car)
bp.get("")(cars_controller.get_all_cars)
bp.get("/<string:license_plate>")(cars_controller.search_car)
bp.patch("/<string:chassis>")(cars_controller.update_car)
bp.delete("/<string:chassis>")(cars_controller.remove_car)
bp.get("")(cars_controller.available_car)