from sqlite3 import IntegrityError
from flask import request, jsonify, current_app
from dotenv import load_dotenv
from http import HTTPStatus
from werkzeug.exceptions import NotFound
import os, json
from app.controllers.address_controller import create_address
from app.models.address_model import Address
from app.models.state_model import States

from app.models.users_model import Users

from app.configs.database import db

load_dotenv()

attributes = json.loads(os.getenv('ATTRIBUTES_USER'))

def create_user():
    data = request.get_json()

    address = data.pop("address")

    returned_address = create_address(address, "create_user")

    if type(returned_address) == tuple:
        if returned_address[1]==0:
            return {'error': f"Missing keys for address: {returned_address[0]}"}, HTTPStatus.CONFLICT
        else:
            return {"error": f"Address attibutes must be string: {returned_address[0]}"}, HTTPStatus.CONFLICT

    missing_keys = []

    for attribute in attributes:
        if attribute not in data.keys():
            missing_keys.append(attribute)
    
    if len(missing_keys)>0:
        return {"error":f"Missing keys for user: {missing_keys}"}, HTTPStatus.BAD_REQUEST
    
    for attribute in data.items():
        if type(attribute[0])!= str:
            return {"error":f"{attribute[0]} must be a string"}, HTTPStatus.BAD_REQUEST
    
    try:
        user = Users(**data)
        user.id_address = returned_address["id"]
    
    except TypeError:
        return {"error":"Type error bad request"}, HTTPStatus.BAD_REQUEST

    try:
        db.session.add(user)
        db.session.commit()

        completed_address = []
        completed_address.append(returned_address)

        user_keys = ["cnh", "cpf", "name", "email", "phone", "category_cnh", "user_address"]
        user_values = [user.cnh, user.cpf, user.name, user.email, user.phone, user.category_cnh, completed_address]

        response = dict(zip(user_keys, user_values))

    except IntegrityError:
        return {"error":"CNH, CPF, email or phone already registred"}, HTTPStatus.CONFLICT
    
    return jsonify(response), HTTPStatus.CREATED


def get_users():
    users = Users.query.all()
    all_users = []
    for user in users:

        db_state = States.query.filter_by(state_id= user.user_address[0].state_id).one()
        user_address_keys = ["address_id", "street", "number", "district", "zip_code", "city", "reference", "state"]
        user_address_values = [user.user_address[0].address_id,user.user_address[0].street, user.user_address[0].number, user.user_address[0].district, user.user_address[0].zip_code, user.user_address[0].city, user.user_address[0].reference, db_state.name]

        user_address_response = dict(zip(user_address_keys, user_address_values))
        completed_address = []
        completed_address.append(user_address_response)

        keys = ["cnh", "cpf", "name", "email", "phone", "category_cnh", "user_address"]
        values = [user.cnh, user.cpf, user.name, user.email, user.phone, user.category_cnh, completed_address]
        response = dict(zip(keys, values))
        all_users.append(response)
    
        
    if not users:
        return {'error': 'users not found'}, HTTPStatus.NOT_FOUND

    return jsonify(all_users), HTTPStatus.OK


def patch_users(cnh):
    
    data = request.get_json()
    user = Users.query.get(cnh)
    not_changed_keys = ["cnh", "cpf"]
    for keys in not_changed_keys:
        if keys in data.keys():
            data.pop(keys)

    old_address = Address.query.filter_by(address_id = user.id_address).one()
    new_address = {}
    
    if "address" in data.keys():
        address = data.pop("address")
        if "street" in address.keys():
            new_address["street"] = address["street"]
        else:
            new_address["street"] = old_address.street
        if "number" in address.keys():
            new_address["number"] = address["number"]
        else:
            new_address["number"] = old_address.number
        if "district" in address.keys():
            new_address["district"] = address["district"]
        else:
            new_address["district"] = old_address.district
        if "zip_code" in address.keys():
            new_address["zip_code"] = address["zip_code"]
        else:
            new_address["zip_code"] = old_address.zip_code
        if "city" in address.keys():
            new_address["city"] = address["city"]
        else:
            new_address["city"] = old_address.city
        if "state" in address.keys():
            new_address["state"] = address["state"]
        else:
            old_state = States.query.filter_by(state_id = old_address.state_id).one()
            new_address["state"] = old_state.name
        if "reference" in address.keys():
            new_address["reference"] = address["reference"]
        else:
            new_address["reference"] = old_address.reference

       
        returned_address = create_address(new_address, "update_user")

        id_address = returned_address["id"]
        new_id_address ={"id_address":id_address}
        for key, value in new_id_address.items():
            setattr(user, key, value)
        current_app.db.session.add(user)
        current_app.db.session.commit()

    else: 
        old_state = States.query.filter_by(state_id = old_address.state_id).one()
        returned_address = {"state":old_state.name}
    
    
    
        
    for key, value in data.items():
        setattr(user, key, value)

    current_app.db.session.add(user)
    current_app.db.session.commit()

    user_address_keys = ["address_id", "street", "number", "district", "zip_code", "city", "reference", "state"]
    user_address_values = [user.user_address[0].address_id,user.user_address[0].street, user.user_address[0].number, user.user_address[0].district, user.user_address[0].zip_code, user.user_address[0].city, user.user_address[0].reference, returned_address["state"]]
    
    user_address_response = dict(zip(user_address_keys, user_address_values))

    completed_address = []
    completed_address.append(user_address_response)

    

    keys = ["cnh", "cpf", "name", "email", "phone", "category_cnh", "user_address"]
    values = [user.cnh, user.cpf, user.name, user.email, user.phone, user.category_cnh, completed_address]

    response = dict(zip(keys, values))

    return jsonify(response), HTTPStatus.OK


def delete_user(cnh):
    user = Users.query.get(cnh)

    try:
        current_app.db.session.delete(user)
        current_app.db.session.commit()
    except NotFound:
        return {'error': f'user cnh {cnh} not found'}, HTTPStatus.NOT_FOUND

    return {'message': f'user cnh {cnh} deleted'}, HTTPStatus.OK


def get_a_user(cnh):

    get_user = Users.query.get(cnh)

    try:

        db_state = States.query.filter_by(state_id= get_user.user_address[0].state_id).one()
        
        user_address_keys = ["address_id", "street", "number", "district", "zip_code", "city", "reference", "state"]
        user_address_values = [get_user.user_address[0].address_id,get_user.user_address[0].street, get_user.user_address[0].number, get_user.user_address[0].district, get_user.user_address[0].zip_code, get_user.user_address[0].city, get_user.user_address[0].reference, db_state.name]
        
        user_address_response = dict(zip(user_address_keys, user_address_values))
        
        completed_address = []
        completed_address.append(user_address_response)

        keys = ["cnh", "cpf", "name", "email", "phone", "category_cnh", "user_address"]
        values = [get_user.cnh, get_user.cpf, get_user.name, get_user.email, get_user.phone, get_user.category_cnh, completed_address]

        response = dict(zip(keys, values))
        


        return jsonify(response), HTTPStatus.OK
    except AttributeError:
        return {'error': f'user cnh {cnh} not found'}, HTTPStatus.NOT_FOUND