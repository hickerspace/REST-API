from flask import jsonify
from logger import log
import os

def announce(lang, text):
	if lang in ['de', 'en']:
		os.system('bash /var/www/hickerspace.org/espeak/espeak_%s.sh \'%s\'' % (lang, text))
		message = {'status': 'Ok'}
		resp = jsonify(message)
	else:
		message = {'message': 'Language not found.'}
		resp = jsonify(message)
		resp.status_code = 403

	return resp

