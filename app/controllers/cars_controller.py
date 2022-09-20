from dotenv import load_dotenv
from flask import current_app, request, jsonify
import os
import json
from http import HTTPStatus
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError

from app.models.cars_model import Cars
from app.models.category_car_model import Category_car
from app.configs.database import db


load_dotenv()

attributes = json.loads(os.getenv('ATTRIBUTES_CAR'))

def create_car():
    data = request.get_json()

    category_keys = ['body_types', 'fuel_type', 'engine_power', 'km_per_liter', 'allowed_category_cnh', 'differentials']

    missing_category_keys = []

    for item in category_keys:
        if item not in data.keys():
            missing_category_keys.append(item)
        if len(missing_category_keys) != 0:
            return {'Error': f'missing keys: {missing_category_keys}'}


    category = {
        'body_types': data.pop('body_types'),
        'fuel_type': data.pop('fuel_type'),
        'engine_power': data.pop('engine_power'),
        'km_per_liter': data.pop('km_per_liter'),
        'allowed_category_cnh': data.pop('allowed_category_cnh'),
        'differentials': data.pop('differentials')
    }

    body = Category_car.query.filter_by(body_types=category['body_types']).first()   
    fuel = Category_car.query.filter_by(fuel_type=category['fuel_type']).first()
    engine = Category_car.query.filter_by(engine_power=category['engine_power']).first()
    km = Category_car.query.filter_by(km_per_liter=category['km_per_liter']).first()
    allowed_cnh = Category_car.query.filter_by(allowed_category_cnh=category['allowed_category_cnh']).first()
    differentials = Category_car.query.filter_by(differentials=category['differentials']).first()

    if body != None and fuel != None and engine != None and km != None and allowed_cnh != None and differentials != None:
        category_dict = {
            'category_id': body.category_id
        }
    else:
        created_category = Category_car(**category)
        db.session.add(created_category)
        db.session.commit()
        category_dict = {
            'category_id': created_category.category_id
        }

    try:
        car = Cars(**data, **category_dict)
    except TypeError as e:
        return {'Error': 'Type error bad request'}, HTTPStatus.BAD_REQUEST

    if len(data.get('chassi')) != 17:
        return {'Error': f'Chassis field must be 17 characters long'}, HTTPStatus.BAD_REQUEST


    missing_keys = []

    for attribute in attributes:
        if attribute not in data.keys():
            missing_keys.append(attribute)

    if len(missing_keys) > 0:
        return {'Error': f'Missing Keys: {missing_keys}'}, HTTPStatus.BAD_REQUEST


    exceptions_keys_data = ['current_km', 'daily_rental_price', 'daily_fixed_km']

    for attribute in data.items():

        if attribute[0] not in exceptions_keys_data:
            if type(attribute[1]) != str:
                return {'Error': f'{attribute[0]} must be a string'}, HTTPStatus.BAD_REQUEST
        else:
            if attribute[0] == 'daily_fixed_km':
                if type(attribute[1]) != int:
                    return {'Error': f'{attribute[0]} must be a int number'}, HTTPStatus.BAD_REQUEST
            else:
                if type(attribute[1]) != float:
                    return {'Error': f'{attribute[0]} must be a float number'}, HTTPStatus.BAD_REQUEST

    try:
        db.session.add(car)
        db.session.commit()
    except IntegrityError:
        return {'Error': 'chassi or license_plate already registered'}, HTTPStatus.CONFLICT

    car.licensing_expiration = car.licensing_expiration.strftime("%d/%m/%Y")
    
    return jsonify(car), HTTPStatus.CREATED
    


def get_all_cars():
    available = request.args.get('available')
    if available:
        possible_keys = ['true', 'false']

        if not available in possible_keys:
            return {'Error': 'Value passed by parameter is not allowed. Check the query params and try again'}, HTTPStatus.BAD_REQUEST


        cars_search = Cars.query.filter_by(available=available).all()

        return jsonify(cars_search), HTTPStatus.OK
    
    session: Session = db.session
    base_query = session.query(Cars)
    record_all_cars = base_query.all()

    if not record_all_cars:
        return {'Error': 'No data found'}, HTTPStatus.NOT_FOUND
    
    if not record_all_cars:
        return {'Error': 'Records not found'}, HTTPStatus.NOT_FOUND

    return jsonify(record_all_cars), HTTPStatus.OK


def update_car(chassi):
    data = request.get_json()

    if len(chassi) != 17:
            return {'Error': f'Chassis field must be 17 characters long'}, HTTPStatus.BAD_REQUEST


    car_update = Cars.query.get(chassi)

    print(car_update)

    if not car_update:
        return {'Error': f'Records not found'}, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(car_update, key, value)


    current_app.db.session.add(car_update)
    current_app.db.session.commit()


    return "", HTTPStatus.NO_CONTENT


def remove_car(chassi):
    data = request.get_json()

    if len(chassi) != 17:
        return {'Error': f'Chassis field must be 17 characters long'}, HTTPStatus.BAD_REQUEST
    
    car_delete = Cars.query.filter_by(chassi=chassi)


    if not car_delete.all():
        return {'Error': f'Records not found'}, HTTPStatus.NOT_FOUND

    car_delete.delete()
    current_app.db.session.commit()

    return "", HTTPStatus.NO_CONTENT



def search_car(license_plate):

    license_plate_upper = license_plate.upper() 

    cars_search = Cars.query.filter(Cars.license_plate.like(f'%{license_plate_upper}%'))

    print(cars_search)
    print(cars_search.all())

    if not cars_search.all():
        return {'Error': f'Records not found'}, HTTPStatus.NOT_FOUND
        

    car_search = cars_search.all()
    
    return jsonify(car_search), HTTPStatus.OK


def available_car():
    available = request.args.get('available')

    possible_keys = ['true', 'false']

    if not available in possible_keys:
        return {'Error': 'Value passed by parameter is not allowed. Check the query params and try again'}, HTTPStatus.BAD_REQUEST


    cars_search = Cars.query.filter_by(available=available)

    return jsonify(cars_search), HTTPStatus.OK