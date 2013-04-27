#!/usr/bin/python
# -*- coding: utf-8 -*-

from werkzeug.contrib.atom import AtomFeed
from conf import *
import tweepy, re, httplib2, simplejson

def resolve(url, expanded):
	h = httplib2.Http()
	h.follow_redirects = False

	try:
		target = h.request(url, 'HEAD')[0]['location']
	except KeyError:
		target = url

	with open(EXPANDED_URLS, 'w') as f:
		expanded[url] = target
		f.write(simplejson.dumps(expanded))

	return target


def expand(text):
	urlMatch = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
	matches = urlMatch.findall(text)
	matches = map(lambda match: match[0], matches)

	with open(EXPANDED_URLS, 'r') as f:
		expanded = simplejson.loads(f.read())

		for url in matches:
			if url in expanded:
				text = text.replace(url, expanded[url])
			else:
				text = text.replace(url, resolve(url, expanded))

		return text


def getUserTimeline(screenName, feedUrl):
	# create Twitter connection
	auth = tweepy.OAuthHandler(TWIT_CONSUMER_KEY, TWIT_CONSUMER_SECRET)
	auth.set_access_token(TWIT_ACCESS_TOKEN, TWIT_ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)

	feed = AtomFeed('Twitter / %s' % screenName,
		links=[{'href': 'http://twitter.com/%s' % screenName}],
		subtitle='Twitter updates from %s.' % screenName, feed_url=feedUrl)

	for status in api.user_timeline(screenName):
		title = expand(status.text)
		if title[:4] == "RT @":
			title = u"♻ %s" % title[3:]

		feed.add(title, title,
			content_type='html',
			author=status.source,
			url="http://twitter.com/%s/statuses/%s" % (status.author.screen_name, status.id_str),
			updated=status.created_at,
			published=status.created_at)

	return feed.get_response()

