from functools import wraps
from flask import request, jsonify
from conf import username, password

def check_auth(user, pw):
	return user == username and pw == password

def authenticate(msg='Authenticate.'):
	resp = jsonify({'message': msg})
	resp.status_code = 401
	resp.headers['WWW-Authenticate'] = 'Basic realm="API credentials needed to access this resource."'

	return resp

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		# require ssl for api requests with auth
		if "https://" not in request.url:
			message = {'message': 'Resouces requiring authentication also require ssl.'}
			resp = jsonify(message)
			resp.status_code = 403
			return resp

		auth = request.authorization
		if not auth: 
			return authenticate()

		elif not check_auth(auth.username, auth.password):
			return authenticate("Authentication Failed.")

		return f(*args, **kwargs)

	return decorated


