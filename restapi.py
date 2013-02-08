from flask import Flask, url_for, request, jsonify
from auth import requires_auth
from misc import parameters_given
from logger import log
import info, announce, room
import os

app = Flask(__name__)

@app.route('/')
def api_root():
	return 'Welcome to the Hickerspace REST API. See http://hickerspace.org/wiki/REST-API for documentation.'

@app.route('/info')
def api_info():
	return jsonify(info.info())

@app.route('/announce')
@requires_auth
@parameters_given(['lang', 'text'])
def api_announce():
	lang = request.args.get('lang')
	text = request.args.get('text')
	return announce.announce(lang, text)

@app.route('/room')
def api_room():
	return jsonify(room.getStatus())

@app.route('/submit-room')
@requires_auth
@parameters_given(['people'])
def api_submit_room():
	people = request.args.get('people')
	return room.submitStatus(people)


if __name__ == '__main__':
	app.run()

