Python (flask) implementation of our REST-API.

Overview
========

* room status (for SpaceAPI etc.)
* extended information about our hackspace
* audio announcement system via long polling
* LED ticker via long polling
* Mate-O-Meter (still to come)
* MUC (xmpp) status
* Wiki status (just redirects)

Dependencies
============

* flask
* [ledticker.py](https://github.com/hickerspace/ledticker/blob/master/ledticker.py)

Notes
=====
* Enable WSGIPassAuthorization to pass through authorisation headers:
http://code.google.com/p/modwsgi/wiki/ConfigurationDirectives#WSGIPassAuthorization
