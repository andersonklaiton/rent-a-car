from http import HTTPStatus
from app.exception.missing_key import MissingKeyError
from app.exception.invalid_date import InvalidDateError

from app.services.error_treatment import filter_keys, missing_key
from app.models.maintenance_car_model import Maintenance
from app.models.cars_model import Cars
from app.configs.database import db

from flask import request, jsonify

def create_maintenance():
    data = request.get_json()
    incoming_keys = data.keys()
    keys = Maintenance.keys
    format_date = Maintenance.format_date
    car = Cars.query.filter_by(license_plate=data["car_license_plate"]).one_or_none()

    if car == None:
        return {'Error': 'car not found'}, HTTPStatus.NOT_FOUND
    
    try:
        maintenance = Maintenance(**data)
        filter_keys(incoming_keys, keys)
        
        missing_key(incoming_keys, keys)

        db.session.add(maintenance)
        db.session.commit()

        maintenance.last_maintenance = format_date(maintenance.last_maintenance)
        maintenance.next_maintenance = format_date(maintenance.next_maintenance)

        return jsonify(maintenance), 201

    except KeyError as e:
        return e.args[0], 400

    except MissingKeyError as e: 
        return e.args[0], 400
    
    except InvalidDateError as e:
        return e.args[0], 400


def update_maintenance(id):
    data = request.get_json()
    incoming_keys = data.keys()
    keys = Maintenance.keys
    format_date = Maintenance.format_date
    car = Cars.query.filter_by(license_plate=data['car_license_plate']).one_or_none()

    if car == None:
        return {'Error': 'car not found'}, HTTPStatus.NOT_FOUND

    try:
        maintenance = Maintenance.query.get(id)

        for key, value in data.items():
            setattr(maintenance, key, value)

        filter_keys(incoming_keys, keys)
        
        db.session.add(maintenance)
        db.session.commit()

        maintenance.last_maintenance = format_date(maintenance.last_maintenance)
        maintenance.next_maintenance = format_date(maintenance.next_maintenance)
        
        return jsonify(maintenance), 200
    
    except KeyError as e:
        return e.args[0], 400
    
    except InvalidDateError as e:
        return e.args[0], 400

def get_maintenance_plate(plate):
    data = Maintenance.query.filter_by(car_license_plate=plate).all()
    car = Cars.query.filter_by(license_plate=plate).all()

    if not car:
        return {'Error': 'car not found'}, HTTPStatus.NOT_FOUND

    if not data:
        return {'Error': 'no maintenance found for this car'}, HTTPStatus.NOT_FOUND

    format_date = Maintenance.format_date

    for item in data:
        item.last_maintenance = format_date(item.last_maintenance)
        item.next_maintenance = format_date(item.next_maintenance)



    return jsonify(data), 200

