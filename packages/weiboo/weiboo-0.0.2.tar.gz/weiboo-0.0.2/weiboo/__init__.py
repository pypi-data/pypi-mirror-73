#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'weiboo'
import yaml
import cached_url
import urllib
import re

def isUser(key):
	try:
		int(key)
		return True
	except:
		return False

def getSearchUrl(key):
	if isUser(key):
		user = int(key)
		return 'https://m.weibo.cn/api/container/getIndex?type=uid&value=%d&containerid=107603%d' \
			% (user, user)
	content_id = urllib.request.pathname2url('100103type=1&q=' + key)
	return 'https://m.weibo.cn/api/container/getIndex?containerid=%s&page_type=searchall' % content_id

def clearUrl(url):
	return url.split('?')[0]

def getSingleCount(card):
	return (int(card['reposts_count']) + 
			int(card['comments_count']) + 
			int(card['attitudes_count']))

def getCount(card):
	card = card.get('mblog', card)
	count = getSingleCount(card)
	if 'retweeted_status' in card:
		count += getSingleCount(card['retweeted_status']) / 3
	return count

def getTextHash(card):
	result = []
	for x in card.get('text', ''):
		if re.search(u'[\u4e00-\u9fff]', x):
			result.append(x)
			if len(result) > 10:
				break
	return ''.join(result)

def getHash(card):
	card = card.get('mblog', card)
	if card.get('retweeted_status'):
		return getTextHash(card.get('retweeted_status'))
	return getTextHash(card)

def sortedResult(result):
	to_sort = []
	for url, card in result.items():
		to_sort.append((getCount(card), (url, card)))
	to_sort.sort(reverse=True)
	return [item[1] for item in to_sort]

def getResultDict(content):
	result = {}
	for card in content['data']['cards']:
		if 'scheme' in card:
			url = clearUrl(card['scheme'])
			if '/status/' in url:
				result[url] = card
	return result

# result is approximately sorted by like
def search(key, force_cache=False, sleep=0): 
	url = getSearchUrl(key)
	content = cached_url.get(url, force_cache=force_cache, 
		sleep = sleep)
	content = yaml.load(content, Loader=yaml.FullLoader)
	result = getResultDict(content)
	return sortedResult(result)
