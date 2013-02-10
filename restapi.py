from flask import Flask, url_for, request, jsonify, redirect
from auth import requires_auth
from misc import parameters_given
from logger import log
import info, longpolling, room, muc
from conf import *
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
	return longpolling.announce(lang, text)

@app.route('/room')
def api_room():
	return jsonify(room.getStatus())

@app.route('/submit-room')
@requires_auth
@parameters_given(['people'])
def api_submit_room():
	people = request.args.get('people')
	return room.submitStatus(people)

@app.route('/muc')
def api_muc():
	return jsonify(muc.mucStatus())

@app.route('/wiki/new')
def api_wiki_new():
	return redirect('http://hickerspace.org/wiki/New.json')

@app.route('/wiki/userspace')
def api_wiki_userspace():
	return redirect('http://hickerspace.org/wiki/Userspace.json')

@app.route('/wiki/updated')
def api_wiki_updated():
	return redirect('http://hickerspace.org/wiki/Updated.json')

@app.route('/long-polling')
@requires_auth
def api_long_polling():
	return longpolling.longPolling()



if __name__ == '__main__':
	app.run()

