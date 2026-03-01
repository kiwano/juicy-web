#!/usr/bin/python

# This program downloads feeds from rss_feeds and adds new items to rss_data
# rss_feeds schema should be: name text, url text, lastupdate timestamp
# rss_data schema should be: name text, update_time timestamp, title text, title_url text, item_title text, item_url text

from time import mktime, sleep
from datetime import datetime
import feedparser
import config
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

class weather_display():

  def __init__(self):
    self.db_engine = create_engine(config.db)
    Session = sessionmaker(bind=self.db_engine)
    self.session = Session()
    self.metadata = MetaData()
    self.metadata.create_all(self.db_engine)
    self.metadata.reflect(self.db_engine)
    self.metar_table = Table('weather_metar', self.metadata, autoload_with=self.db_engine)
    self.fpcn_table = Table('weather_fpcn', self.metadata, autoload_with=self.db_engine)

  def get_metar_weather(self, station):
    rq = self.metar_table.select().where(
      self.metar_table.c.station == station).order_by(
      desc(self.metar_table.c.year)).order_by(
      desc(self.metar_table.c.month)).order_by(
      desc(self.metar_table.c.timecode)).limit(1)
    entries = self.session.execute(rq)
    return entries

  def juicy_display_metar(self, station, entries):
    if entries.rowcount == 1:
      for entry in entries.mappings():
        station = entry['station']
        timecode = '%06d' % entry['timecode']
        report = entry['report']
        url = entry['url']
    else:
      print('METAR DB error for ' + station + '<br>')
      return
    if url == None:
      print(station + ' ' + timecode + 'Z ' + report + '<br>')
    else:
      print('<b><a href="'+url+'">' + station + '</a></b> ' + timecode + 'Z ' + report + '<br>')

  def get_fpcn_weather(self, id):
    #rq = select([self.fpcn_table]).where(
    rq = self.fpcn_table.select().where(
      self.fpcn_table.c.fpcn == id).order_by(
      desc(self.fpcn_table.c.year)).order_by(
      desc(self.fpcn_table.c.month)).order_by(
      desc(self.fpcn_table.c.timecode)).limit(1)
    entries = self.session.execute(rq)
    return entries

  def juicy_display_fpcn(self, forecast, entries):
    if entries.rowcount == 1:
      for entry in entries.mappings():
        forecast = entry['report']
    else:
      print('Text forecast DB error for ' + forecast)
      return
    print(forecast.replace('\n', '<br>\n') + '<br>')

  def juicy_display_weather(self):
    print('<b>Weather</b>')
    print('<p>')
    for station in config.weatherstations:
      entries = self.get_metar_weather(station)
      self.juicy_display_metar(station, entries)
    print('<p>')
    print('<b>Toronto Forecast:</b><br>')
    for forecast in ['FPCN11', 'FPCN51']:
      entries = self.get_fpcn_weather(forecast)
      self.juicy_display_fpcn(forecast, entries)
    print('<p>')
    print('<a href="http://meteo.gc.ca/marine/region_e.html?mapID=11">Marine</a><br>')
    entries = self.get_fpcn_weather('FQCN13')
    self.juicy_display_fpcn('FQCN13', entries)
    entries = self.get_fpcn_weather('FQCN53')
    self.juicy_display_fpcn('FQCN53', entries)
    print('<a href="http://www.glerl.noaa.gov/res/glcfs/">Surface temps, currents, etc.</a><br>')
    print('<p>')

