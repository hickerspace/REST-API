import logging

logging.basicConfig(
	level=logging.DEBUG,
	filename='hickerspace.org/wsgi-scripts/restapi/restapi.log',
	format='%(asctime)s %(levelname)-8s %(message)s',
	datefmt='%d.%m.%Y %H:%M:%S')

log = logging.getLogger('REST-API')

