from flask import Blueprint

from app.controllers import rental_cars_controller


bp = Blueprint('rentals', __name__, url_prefix='/rentals')

bp.post('')(rental_cars_controller.rent_car)
bp.patch('')(rental_cars_controller.return_car)
bp.patch('/update_return')(rental_cars_controller.uptade_return_date)
bp.get('')(rental_cars_controller.get_all)
bp.get('/plate/<plate>')(rental_cars_controller.get_by_plate)
bp.get('/all/<cnh>')(rental_cars_controller.get_all_by_users)
bp.get('/current/<cnh>')(rental_cars_controller.get_current_rental_by_user)