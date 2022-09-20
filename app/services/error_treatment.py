from app.exception.missing_key import MissingKeyError
from app.exception.invalid_date import InvalidDateError
from datetime import datetime

def filter_keys(incoming_keys, right_keys):
	wrong_keys = list(incoming_keys - right_keys)
	if wrong_keys:
		raise KeyError(
			{
				"error": "invalid_keys",
				"expected_keys": right_keys,
				"wrong_keys": wrong_keys
			}
		)

def missing_key(incoming_keys, right_keys):
	missing_key = list(right_keys - incoming_keys)
	if missing_key:
		raise MissingKeyError(
			{
				"missing_key": missing_key
			}
		)

# def validate_date(*args):
# 	data = list(args)

# 	for item in data:
# 		if type(item) is str:
# 			try:
# 				datetime.strptime(item, '%d/%m/%Y')

# 			except:
# 				raise InvalidDateError(
# 					{
# 						"invalid_date": item
# 					}
# 				)