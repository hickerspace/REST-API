from functools import update_wrapper
from flask import request, jsonify

"""
Checks if given parameters are available as GET or POST variables.
"""
def parameters_given(params):
	def decorator(fn):
		def wrapped_function(*args, **kwargs):
			for param in params:
				if param not in request.args:
					message = {'message': 'Please define all non-optional arguments.'}
					resp = jsonify(message)
					resp.status_code = 403
					return resp

			return fn(*args, **kwargs)
		return update_wrapper(wrapped_function, fn)
	return decorator


