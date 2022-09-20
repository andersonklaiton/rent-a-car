from http import HTTPStatus
from flask import current_app, jsonify
from app.models.address_model import Address
from app.models.state_model import States

def create_state(state):
    session = current_app.db.session()
    state_db: States = States.query.filter_by(name = state).one_or_none()

    if not state_db:
        state_db = States(name = state)
        session.add(state_db)
        session.commit()

    return state_db.state_id

def get_states():
    states_list=[]
    states_ids = []
    address_list = []
    completed_state_list = []
    states = States.query.all()

    for state in states:
        states_ids.append(state.state_id)
        states_list.append(state.name)
    
    addressess = Address.query.all()

    for state_id in states_ids:
        for address in addressess:
            if address.state_id == state_id:
                address_list.append(address)
            list_address_list=[]
            list_address_list.append(address_list)
            response = dict(zip(states_list[state_id-1:], list_address_list))

        completed_state_list.append(response)
        address_list=[]

    return jsonify(completed_state_list), HTTPStatus.OK