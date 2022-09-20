from flask import Blueprint

from app.controllers import maintenance_controller

bp = Blueprint("maintenance", __name__, url_prefix="/maintenance")

bp.post("")(maintenance_controller.create_maintenance)
bp.get("/<plate>")(maintenance_controller.get_maintenance_plate)
bp.patch("/<id>")(maintenance_controller.update_maintenance)