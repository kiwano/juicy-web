#!/usr/bin/python3

# This module reads rss feed data from a database table (rss_data), and formats it for inclusion on a web page
# rss_data schema should be: name text, update_time timestamp, title text, title_url text, item_title text, item_url text

from time import mktime, sleep
from datetime import datetime
import feedparser
import config
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

class rss_display():

  def __init__(self):
    self.db_engine = create_engine(config.db)
    Session = sessionmaker(bind=self.db_engine)
    self.session = Session()
    self.metadata = MetaData()
    self.metadata.create_all(self.db_engine)
    self.metadata.reflect(self.db_engine)
    self.feed_table = Table('rss_data', self.metadata, autoload_with=self.db_engine)

  def get_feed_entries(self, limit=15, offset=0):
    rq = self.feed_table.select().order_by(desc(self.feed_table.c.update_time)).limit(limit).offset(offset)
    entries = self.session.execute(rq)
    return entries

  def juicy_feed_entries(self, limit=15, offset=0):
    entries = self.get_feed_entries(limit, offset)
    for entry in entries.mappings():
      title = entry['title']
      title_url = entry['title_url']
      item_title = entry['item_title']
      item_url = entry['item_url']
      print('<hr><b><a href="' + title_url + '">' + title + '</a>:</b> <a href="' + item_url + '" rel="nofollow">' + item_title + '</a>')

