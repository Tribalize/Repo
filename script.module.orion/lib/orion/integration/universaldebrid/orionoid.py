# -*- coding: utf-8 -*-

'''
	Orion Addon

	THE BEERWARE LICENSE (Revision 42)
	Orion (orionoid.com) wrote this file. As long as you retain this notice you
	can do whatever you want with this stuff. If we meet some day, and you think
	this stuff is worth it, you can buy me a beer in return.
'''

from ..scraper import Scraper
from ..common import get_rd_domains

from orion import *
from orion.modules.oriontools import *

import base64
import json
import time
import sys
import os
import xbmc
import xbmcvfs
import xbmcaddon

class orionoid(Scraper):

	name = 'Orion'
	domain = ['https://orionoid.com']
	sources = []

	TimeDays = 86400

	SizeMegaByte = 1048576
	SizeGigaByte = 1073741824

	SettingNone = 0
	SettingStreamProvider = 1
	SettingStreamHoster = 2
	SettingStreamSeeds = 3
	SettingFileSize = 4
	SettingFilePack = 5
	SettingMetaEdition = 6
	SettingMetaRelease = 7
	SettingMetaUploader = 8
	SettingVideoQuality = 9
	SettingVideoCodec = 10
	SettingVideo3D = 11
	SettingAudioChannels = 12
	SettingAudioSystem = 13
	SettingAudioCodec = 14
	SettingAudioLanguages = 15
	SettingPopularity = 16
	SettingAge = 17

	Keys = {
		'default' : 'Vm5sQ1VVbEZNR2RSZVVFeVNVVm5aMU5wUWs5SlJVVm5VbmxDVlVsRlVXZFZRMEpOU1VWalowNXBRa3hKUlZsblVXbENSVWxGWTJkU1EwSkxTVVJuWjFORFFrNUpSRTFuVTNsQ1NVbEZSV2RUYVVFdw==',
		'plugin.video.asgard' : 'VTNsQ1IwbEZVV2RTVTBKSlNVVlJaMUZUUWxsSlJHTm5VbE5DVTBsRlJXZFRhVUpPU1VWdloxUkRRa1JKUkdkblRtbENUMGxGVFdkUFUwSkVTVVpSWjFSRFFrbEpSVWxuVW1sQk5VbEdTV2RUUTBKTg==',
	}

	def __init__(self):
		self.addon = xbmcaddon.Addon('script.module.universaldebrid')
		self.language = ['ab', 'aa', 'af', 'ak', 'sq', 'am', 'ar', 'an', 'hy', 'as', 'av', 'ae', 'ay', 'az', 'bm', 'ba', 'eu', 'be', 'bn', 'bh', 'bi', 'nb', 'bs', 'br', 'bg', 'my', 'ca', 'ch', 'ce', 'ny', 'zh', 'cv', 'kw', 'co', 'cr', 'hr', 'cs', 'da', 'dv', 'nl', 'dz', 'en', 'eo', 'et', 'ee', 'fo', 'fj', 'fi', 'fr', 'ff', 'gd', 'gl', 'lg', 'ka', 'de', 'el', 'gn', 'gu', 'ht', 'ha', 'he', 'hz', 'hi', 'ho', 'hu', 'is', 'io', 'ig', 'id', 'ia', 'ie', 'iu', 'ik', 'ga', 'it', 'ja', 'jv', 'kl', 'kn', 'kr', 'ks', 'kk', 'km', 'ki', 'rw', 'rn', 'kv', 'kg', 'ko', 'ku', 'kj', 'ky', 'lo', 'la', 'lv', 'li', 'ln', 'lt', 'lu', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'gv', 'mi', 'mr', 'mh', 'mn', 'na', 'nv', 'ng', 'ne', 'nd', 'se', 'no', 'ii', 'nn', 'oc', 'oj', 'or', 'om', 'os', 'pi', 'ps', 'fa', 'pl', 'pt', 'pa', 'qu', 'ro', 'rm', 'ru', 'sm', 'sg', 'sa', 'sc', 'sr', 'sn', 'sd', 'si', 'cu', 'sk', 'sl', 'so', 'nr', 'st', 'es', 'su', 'sw', 'ss', 'sv', 'tl', 'ty', 'tg', 'ta', 'tt', 'te', 'th', 'bo', 'ti', 'to', 'ts', 'tn', 'tr', 'tk', 'tw', 'uk', 'ur', 'ug', 'uz', 've', 'vi', 'vo', 'wa', 'cy', 'fy', 'wo', 'xh', 'yi', 'yo', 'za', 'zu']
		try: self.cachePath = os.path.join(xbmcvfs.translatePath(OrionTools.unicodeDecode(self.addon.getAddonInfo('profile'))), 'orion.cache')
		except: self.cachePath = os.path.join(xbmc.translatePath(OrionTools.unicodeDecode(self.addon.getAddonInfo('profile'))), 'orion.cache')
		self.cacheData = None
		try: self.key = orionoid.Keys[xbmcaddon.Addon().getAddonInfo('id')]
		except: self.key = orionoid.Keys['default']

	def _error(self):
		type, value, trace = sys.exc_info()
		try: filename = trace.tb_frame.f_code.co_filename
		except: filename = None
		try: linenumber = trace.tb_lineno
		except: linenumber = None
		try: name = trace.tb_frame.f_code.co_name
		except: name = None
		try: errortype = type.__name__
		except: errortype = None
		try: errormessage = value.message
		except:
			try:
				import traceback
				errormessage = traceback.format_exception(type, value, trace)
			except: pass
		message = str(errortype) + ' -> ' + str(errormessage)
		parameters = [filename, linenumber, name, message]
		parameters = ' | '.join([str(parameter) for parameter in parameters])
		xbmc.log('UNIVERSAL DEBRID ORION [ERROR]: ' + parameters, xbmc.LOGERROR)

	def _settings(self, full = True):
		settings = []
		for i in range(1, 16):
			setting = int(self.addon.getSetting('Orion_info.' + str(i)))
			if full or setting > 0: settings.append(setting)
		return settings

	def _cacheSave(self, data):
		self.cacheData = data
		file = xbmcvfs.File(self.cachePath, 'w')
		file.write(json.dumps(data))
		file.close()

	def _cacheLoad(self):
		if self.cacheData == None:
			file = xbmcvfs.File(self.cachePath)
			self.cacheData = json.loads(file.read())
			file.close()
		return self.cacheData

	def _cacheFind(self, url):
		cache = self._cacheLoad()
		for i in cache:
			if i['url'] == url:
				return i
		return None

	def _link(self, data):
		links = data['links']
		for link in links:
			if link.lower().startswith('magnet:'):
				return link.split('&tr')[0]
		return links[0]

	def _quality(self, data):
		try:
			quality = data['video']['quality']
			if quality in [Orion.QualityHd8k, Orion.QualityHd6k, Orion.QualityHd4k]:
				return '4K'
			elif quality in [Orion.QualityHd2k]:
				return '1440p'
			elif quality in [Orion.QualityHd1080]:
				return '1080p'
			elif quality in [Orion.QualityHd720]:
				return '720p'
			elif quality in [Orion.QualityScr1080, Orion.QualityScr720, Orion.QualityScr]:
				return 'SCR'
			elif quality in [Orion.QualityCam1080, Orion.QualityCam720, Orion.QualityCam]:
				return 'CAM'
		except: pass
		return 'SD'

	def _language(self, data):
		try:
			language = data['audio']['language']
			if 'en' in language: return 'en'
			return language[0]
		except: return 'en'

	def _source(self, data, label = True):
		if data['stream']['type'] == OrionStream.TypeTorrent:
			return 'Torrent'
		elif label:
			try: hoster = data['stream']['hoster']
			except: hoster = None
			if hoster: return hoster
			try: source = data['stream']['source']
			except: source = None
			return source if source else ''
		else:
			try: return data['stream']['source']
			except: return None

	def _size(self, data):
		size = data['file']['size']
		if size:
			if size < orionoid.SizeGigaByte: return '%d MB' % int(size / float(orionoid.SizeMegaByte))
			else: return '%0.1f GB' % (size / float(orionoid.SizeGigaByte))
		return None

	def _seeds(self, data):
		seeds = data['stream']['seeds']
		if seeds:
			seeds = int(seeds)
			return str(seeds) + ' Seed' + ('' if seeds == 1 else 's')
		return None

	def _days(self, data):
		try: days = (time.time() - data['time']['updated']) / float(orionoid.TimeDays)
		except: days = 0
		days = int(days)
		return str(days) + ' Day' + ('' if days == 1 else 's')

	def _popularity(self, data):
		try: popularity = data['popularity']['percent'] * 100
		except: popularity = 0
		return '+' + str(int(popularity)) + '%'

	def scrape(self, type, title = None, year = None, yearEpisode = None, season = None, episode = None, imdb = None, tvdb = None, debrid = None):
		self.sources = []
		try:
			orion = Orion(OrionTools.base64From(OrionTools.base64From(OrionTools.base64From(self.key))).replace(' ', ''))
			if not orion.userEnabled() or not orion.userValid(): raise Exception()
			settings = self._settings(full = False)

			if type == Orion.TypeShow and (season is None or season == ''): raise Exception()

			results = orion.streams(
				type = type,
				idImdb = imdb,
				idTvdb = tvdb,
				numberSeason = season,
				numberEpisode = episode,
				streamType = orion.streamTypes([OrionStream.TypeTorrent]), # Currently only has torrents.
				protocolTorrent = Orion.ProtocolMagnet
			)

			debridDomains = None
			if debrid:
				debridDomains = get_rd_domains()
				debridDomains = [i.lower().split('.', 1)[0] for i in debridDomains]

			for data in results:
				try:
					source = self._source(data, True)
					provider = self._source(data, False)

					info = [self.name]
					for setting in settings:
						if setting == orionoid.SettingStreamProvider:
							try: info.append(data['stream']['source'])
							except: pass
						elif setting == orionoid.SettingStreamHoster:
							try: info.append(data['stream']['hoster'])
							except: pass
						elif setting == orionoid.SettingStreamSeeds:
							try: info.append(self._seeds(data))
							except: pass
						elif setting == orionoid.SettingFileSize:
							try: info.append(self._size(data))
							except: pass
						elif setting == orionoid.SettingFilePack:
							try: info.append('Pack' if data['file']['pack'] else None)
							except: pass
						elif setting == orionoid.SettingMetaEdition:
							try: info.append(data['meta']['edition'])
							except: pass
						elif setting == orionoid.SettingMetaRelease:
							try: info.append(data['meta']['release'])
							except: pass
						elif setting == orionoid.SettingMetaUploader:
							try: info.append(data['meta']['uploader'])
							except: pass
						elif setting == orionoid.SettingVideoQuality:
							try: info.append(data['video']['quality'].upper())
							except: pass
						elif setting == orionoid.SettingVideoCodec:
							try: info.append(data['video']['codec'].upper())
							except: pass
						elif setting == orionoid.SettingVideo3D:
							try: info.append('3D' if data['video']['3d'] else None)
							except: pass
						elif setting == orionoid.SettingAudioChannels:
							try: info.append('%d CH' % data['audio']['channels'] if data['audio']['channels'] else None)
							except: pass
						elif setting == orionoid.SettingAudioSystem:
							try: info.append(data['audio']['system'].upper())
							except: pass
						elif setting == orionoid.SettingAudioCodec:
							try: info.append(data['audio']['codec'].upper())
							except: pass
						elif setting == orionoid.SettingAudioLanguages:
							try: info.append('-'.join(data['audio']['languages'].upper()))
							except: pass
						elif setting == orionoid.SettingPopularity:
							try: info.append(self._popularity(data))
							except: pass
						elif setting == orionoid.SettingAge:
							try: info.append(self._days(data))
							except: pass
					info = [i for i in info if i]

					orion = {}
					try: orion['stream'] = data['id']
					except: pass
					try: orion['item'] = data
					except: pass

					self.sources.append({
						'orion' : orion,
						'scraper' : ' | '.join(info),
						'provider' : provider,
						'source' : source,
						'quality' : self._quality(data),
						'language' : self._language(data),
						'url' : self._link(data),
						'direct' : data['access']['direct'],
						'debridonly' : data['stream']['type'] == OrionStream.TypeTorrent or (not data['access']['direct'] and debrid and source in debridDomains)
					})
				except: self._error()
		except: self._error()
		self._cacheSave(self.sources)
		return self.sources

	def scrape_movie(self, title, year, imdb, debrid = False):
		return self.scrape(type = Orion.TypeMovie, title = title, year = year, imdb = imdb, debrid = debrid)

	def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
		return self.scrape(type = Orion.TypeShow, title = title, year = show_year, yearEpisode = year, season = season, episode = episode, imdb = imdb, tvdb = tvdb, debrid = debrid)
