from flask import request, jsonify, current_app, render_template
from flask_mail import Message, Mail
from dotenv import load_dotenv
from http import HTTPStatus
import os, json
from werkzeug.exceptions import NotFound

from app.models.rental_cars_model import RentalCars
from app.models.cars_model import Cars
from app.models.users_model import Users
from app.models.category_car_model import Category_car
from app.services.error_treatment import filter_keys, missing_key

def rent_car():
    try:
        load_dotenv()

        km_per_day = json.loads(os.getenv('KM_PER_DAY'))
        data = request.get_json()
        keys = RentalCars.create_keys

        filter_keys(data.keys(), keys)
        missing_key(data.keys(), keys)

        car_to_be_rented = Cars.query.filter_by(license_plate=data['car_license_plate']).first_or_404()
        is_cnh_in_database = Users.query.filter_by(cnh=data['customer_cnh']).first_or_404()
        rentals_not_returned = RentalCars.query.filter_by(customer_cnh=data['customer_cnh']).first()
        category = Category_car.query.filter_by(category_id=car_to_be_rented.category_id).one_or_none()
        user_cnh_list = [letter.upper() for letter in is_cnh_in_database.category_cnh]
        car_cnh = [letter.upper() for letter in category.allowed_category_cnh]

        if category == None:
            return {'Error': 'Category not found'}, HTTPStatus.NOT_FOUND

        for letter in user_cnh_list:
            if letter not in car_cnh:
                return {'Error': 'User cnh does not allow him to drive this car'}, HTTPStatus.CONFLICT

        if rentals_not_returned:
            if rentals_not_returned.returned_car == False:
                return {'Error': 'User already rented a car and did not return it yet'}, HTTPStatus.CONFLICT

        if car_to_be_rented.available == False:
            return {'Error': 'Car already rented'}, HTTPStatus.CONFLICT

        plate = data.pop('car_license_plate')
        rental_info = {
            'returned_car': False,
            'initial_km': car_to_be_rented.current_km,
            'total_fixed_km': km_per_day,
            'rental_value': car_to_be_rented.daily_rental_price * data['rental_total_days'],
            'car_license_plate': plate.upper()
        }

        setattr(car_to_be_rented, 'available', False)
        current_app.db.session.add(car_to_be_rented)
        current_app.db.session.commit()
        
        rental_car = RentalCars(**data, **rental_info)

        current_app.db.session.add(rental_car)
        current_app.db.session.commit()

        rental_car.rental_date = rental_car.rental_date.strftime("%d/%m/%Y")
        rental_car.rental_return_date = rental_car.rental_return_date.strftime("%d/%m/%Y")


        def flask_mail(email):
            mail: Mail = current_app.mail
            msg = Message(
                subject="Resumo de sua locação",
                sender=os.getenv("MAIL_USERNAME"),
                recipients=[email],
                html=render_template("email/template.html", name=is_cnh_in_database.name, cnh=rental_car.customer_cnh, plate=rental_car.car_license_plate, rental_date=rental_car.rental_date, return_date=rental_car.rental_return_date, total_days=rental_car.rental_total_days, fixed_km=rental_car.total_fixed_km, initial_km=rental_car.initial_km)

            )
            mail.send(msg)
        flask_mail(is_cnh_in_database.email)

        return jsonify(rental_car)

    except NotFound:
        return {'Error': 'Car or cnh not found!'}, HTTPStatus.NOT_FOUND


def return_car():
    try:
        load_dotenv()

        km_per_day = json.loads(os.getenv('KM_PER_DAY'))
        km_after_limit = json.loads(os.getenv('PRICE_PER_KM_AFTER_LIMIT'))
        day_after_limit = json.loads(os.getenv('PRICE_PER_DAY_AFTER_LIMIT'))
        data = request.get_json()

        keys = RentalCars.return_keys

        filter_keys(data.keys(), keys)
        missing_key(data.keys(), keys)
        
        car_to_be_returned = Cars.query.filter_by(license_plate=data['car_license_plate'].upper()).first_or_404()
        is_cnh_in_database = Users.query.filter_by(cnh=data['cnh']).first_or_404()
        rental_not_returned = RentalCars.query.filter_by(customer_cnh=data['cnh'],returned_car=False).first()

        if not rental_not_returned:
            return {'Error': 'User has no rental pending'}, HTTPStatus.NOT_FOUND

        real_km_per_day = (data['total_returned_km'] - rental_not_returned.initial_km) / data['rental_real_total_days']

        to_pay_per_km = 0
        if real_km_per_day > km_per_day:
            to_pay_per_km = (real_km_per_day - km_per_day) * km_after_limit * data['rental_real_total_days']

        to_pay_per_day = 0
        if data['rental_real_total_days'] > rental_not_returned.rental_total_days:
            to_pay_per_day = (data['rental_real_total_days'] - rental_not_returned.rental_total_days) * day_after_limit
        
        user_info_to_be_patched = {
            'rental_real_return_date': data['rental_real_return_date'],
            'returned_car': True,
            'rental_real_total_days': data['rental_real_total_days'],
            'final_km': data['total_returned_km'] + rental_not_returned.initial_km,
            'total_returned_km': data['total_returned_km'],
            'rental_real_value': rental_not_returned.rental_value + to_pay_per_km + to_pay_per_day
        }

        for key, value in user_info_to_be_patched.items():
            setattr(rental_not_returned, key, value)
        
        setattr(car_to_be_returned, 'available', True)
        setattr(car_to_be_returned, 'current_km', data['total_returned_km'] + rental_not_returned.initial_km)

        current_app.db.session.add(rental_not_returned)
        current_app.db.session.add(car_to_be_returned)
        current_app.db.session.commit()

        rental_not_returned.rental_real_return_date = rental_not_returned.rental_real_return_date.strftime("%d/%m/%Y")
        rental_not_returned.rental_date = rental_not_returned.rental_date.strftime("%d/%m/%Y")
        def flask_mail(email):
            mail: Mail = current_app.mail
            msg = Message(
                subject="Confirmação de devolução",
                sender=os.getenv("MAIL_USERNAME"),
                recipients=[email],
                html=render_template("email/template2.html", name=is_cnh_in_database.name, cnh=rental_not_returned.customer_cnh, plate=rental_not_returned.car_license_plate, rental_date=rental_not_returned.rental_date, real_return_date=rental_not_returned.rental_real_return_date, rental_real_total_days=rental_not_returned.rental_total_days, fixed_km=rental_not_returned.total_fixed_km, final_km=rental_not_returned.final_km, rental_real_value=rental_not_returned.rental_real_value)

            )
            mail.send(msg)
        flask_mail(is_cnh_in_database.email)

        return jsonify(rental_not_returned), HTTPStatus.OK


    except NotFound:
        return {'Error': 'Car or cnh not found'}, HTTPStatus.NOT_FOUND


def uptade_return_date():
    keys_to_be_received = ['cnh', 'car_license_plate', 'rental_return_date', 'rental_total_days']

    data = request.get_json()

    wrong_keys = []
    for item in data.keys():
        if item not in keys_to_be_received:
            wrong_keys.append(item)
        if len(wrong_keys) != 0:
            return {'Error': f'Missing key(s): {wrong_keys}'}, HTTPStatus.BAD_REQUEST
    
    if len(data.keys()) != 4:
        return {'Error': 'This endpoint should receive only the following keys: cnh, car_license_plate and return_date'}, HTTPStatus.BAD_REQUEST
    

    user = Users.query.filter_by(cnh=data['cnh']).one_or_none()
    car = Cars.query.filter_by(license_plate=data['car_license_plate']).one_or_none()
    invoice = RentalCars.query.filter_by(car_license_plate=data['car_license_plate'].upper(),returned_car=False).one_or_none()

    if user == None:
        return {'Error': 'user not found'}, HTTPStatus.NOT_FOUND
    
    if car == None:
        return {'Error': 'car not found'}, HTTPStatus.NOT_FOUND
    
    if invoice == None:
        return {'Error': 'car available in parking lot'}, HTTPStatus.CONFLICT
    
    setattr(invoice, 'rental_return_date', data['rental_return_date'])
    setattr(invoice, 'rental_total_days', data['rental_total_days'])
    setattr(invoice, 'rental_value', car.daily_rental_price * data['rental_total_days'])

    current_app.db.session.add(invoice)
    current_app.db.session.commit()

    invoice.rental_return_date = invoice.rental_return_date.strftime("%d/%m/%Y")

    return jsonify(invoice), HTTPStatus.OK


def get_all():
    all_invoices = RentalCars.query.all()

    return jsonify(all_invoices), HTTPStatus.OK

def get_by_plate(plate):
    try:
        invoice = RentalCars.query.filter_by(car_license_plate=plate.upper(),returned_car=False).first_or_404()

        return jsonify(invoice), HTTPStatus.OK
    
    except NotFound:
        return {'Error': 'Car not found or car not rented'}, HTTPStatus.NOT_FOUND

def get_all_by_users(cnh):
    invoice = RentalCars.query.filter_by(customer_cnh=cnh).all()

    if len(invoice) == 0:
        return {'Error': 'User not found or never rented a car'}, HTTPStatus.NOT_FOUND

    return jsonify(invoice), HTTPStatus.OK

def get_current_rental_by_user(cnh):
    try:
        invoice = RentalCars.query.filter_by(customer_cnh=cnh,returned_car=False).first_or_404()

        return jsonify(invoice), HTTPStatus.OK
    
    except NotFound:
        return {'Error': 'User not found or not renting any car'}, HTTPStatus.NOT_FOUND