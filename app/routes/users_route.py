from flask import Blueprint

from app.controllers import users_controller


bp = Blueprint('users', __name__, url_prefix='/users')

bp.post('')(users_controller.create_user)
bp.get('')(users_controller.get_users)
bp.get('/<string:cnh>')(users_controller.get_a_user)
bp.patch('/<string:cnh>')(users_controller.patch_users)
bp.delete('/<string:cnh>')(users_controller.delete_user)