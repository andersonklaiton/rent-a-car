from flask import Blueprint
from app.controllers import category_car_controller

bp = Blueprint("category",__name__, url_prefix="/categories")

bp.post("")(category_car_controller.create_category_car)