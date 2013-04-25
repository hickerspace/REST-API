from functools import update_wrapper
from flask import request, jsonify
from conf import *

"""
Simple method to check API credentials
"""
def check_auth(username, password):
	for user, pw in API_ACCESS:
		if username == user and password == pw:
			return True

	return False

"""
Basic authentication for protected resources.
Source: "HTTP Basic Auth" by Armin Ronacher
		http://flask.pocoo.org/snippets/8/
"""
def authenticate(msg='Please authenticate.'):
	resp = jsonify({'success': False, 'status': msg})
	resp.status_code = 401
	resp.headers['WWW-Authenticate'] = 'Basic realm="API credentials needed to access this resource."'
	return resp

"""
Basic authentication for protected resources and SSL enforcement.
Source: "HTTP Basic Auth" by Armin Ronacher
		http://flask.pocoo.org/snippets/8/
Changed to require ssl for authentication. Extra argument added to require auth only for POST requests.
"""

def requires_auth(postAuthOnly=False):
	def decorator(f):
		def wrapped_function(*args, **kwargs):
			# require ssl for api requests with auth
			if "https://" not in request.url and not (postAuthOnly and request.method != 'POST'):
				message = { 'success': False, 'status': 'Resources requiring authentication also require ssl.'}
				resp = jsonify(message)
				resp.status_code = 403
				return resp

			if not (request.method != 'POST' and postAuthOnly):
				auth = request.authorization
				if not auth:
					return authenticate()

				elif not check_auth(auth.username, auth.password):
					return authenticate("Authentication Failed.")

			return f(*args, **kwargs)
		return update_wrapper(wrapped_function, f)
	return decorator


