from flask import Blueprint

from app.controllers.mail import flask_mail


bp = Blueprint('mail', __name__, url_prefix="/mail")

bp.get("")(flask_mail)