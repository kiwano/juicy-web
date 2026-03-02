#!/usr/bin/python3

# This program downloads feeds from rss_feeds and adds new items to rss_data
# rss_feeds schema should be: name text, url text, lastupdate timestamp
# rss_data schema should be: name text, update_time timestamp, title text, title_url text, item_title text, item_url text

from time import mktime, sleep
from datetime import datetime, timezone
import feedparser
import config
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


#### Functions

# Save items from the feed in rss_data

def save_feed_item(name, timestamp, feed_title, feed_url, item_title, item_url):
  iq = data_table.insert().values(
    name=name,
    update_time=timestamp,
    title=feed_title,
    title_url=feed_url,
    item_title=item_title,
    item_url=item_url
  )
  session.execute(iq)
  print("adding:", item_title.encode("utf-8"), item_url.encode("utf-8"), "to", name)
  session.commit()


# Return how many rows already exist, and look like the specified item

def test_similar_rows(data_table, name, url):
  sq = data_table.select().where(
    and_(
      data_table.c.name == name,
      data_table.c.item_url == url
    )
  )
  matches = session.execute(sq)
  return len(matches.fetchall())


def process_feed_items(data_table, name, title, url, time, items):
  #print('update for', title, url, 'has %d items' % len(items))

  best_timestamp = datetime.fromtimestamp(0)

  for item in items:
    if ( ("published_parsed" in item) and (item["published_parsed"] != None) ):
      item_timestamp = datetime.fromtimestamp(mktime(item["published_parsed"]))
      best_timestamp = item_timestamp if (item_timestamp > best_timestamp) else best_timestamp
    else:
      item_timestamp = time

    if "link" in item:
      item_title = item.get("title") or item_timestamp.strftime("%Y-%m-%d %H:%M")
      if (test_similar_rows(data_table, name, item["link"]) == 0):
        save_feed_item(name, item_timestamp, title, url, item_title, item["link"])
    else:
      print("Malformed RSS item received:")
      print(item)

  return best_timestamp


def update_feed_in_db(feedtime, itemtime, name):
  updatetime = feedtime if (feedtime > itemtime) else itemtime
  uq = feed_table.update().\
    where(feed_table.c.name == name).\
    values(lastupdate=updatetime)
  session.execute(uq)
  session.commit()


def process_feed_update(feedupdate, data_table, name):
  feedhead = feedupdate.feed
  feedtitle = feedhead["title"]
  feedurl = feedhead["links"][0]["href"]
  #print('downloaded update for %s (at %s)' % (feedtitle, feedurl))

  if ( ("updated_parsed" in feedhead) and (feedhead["updated_parsed"] != None) ):
    feedtime = datetime.fromtimestamp(mktime(feedhead["updated_parsed"]))
    #print('Update timestamp:', feedtime)
  else:
    #print("No update timestamp, using epoch")
    feedtime = datetime.fromtimestamp(0)

  itemtime =  process_feed_items(data_table, name, feedtitle, feedurl, feedtime, feedupdate["items"])
  update_feed_in_db(feedtime, itemtime, name)


def check_bozo_feed(feedupdate):
  #print('checking feedupdate: ', feedupdate)
  if ('feed' in feedupdate) or ('channel' in feedupdate):
    #print('found feed item')
    if 'title' in feedupdate.feed:
      #print('feed item has title object:', feedupdate.feed['title'])
      pass
    else:
      #print('feed item has no title object; bozo is fatal')
      return 0
    if 'links' in feedupdate.feed:
      #print('feed item has links object')
      if len(feedupdate.feed["links"]) > 0:
        #print('there are', len(feedupdate.feed["links"]), 'links')
        if 'href' in feedupdate.feed["links"][0]:
          #print('feed has an url', feedupdate.feed["links"][0]["href"])
          pass
        else:
          #print('feed has no url; bozo is fatal')
          return 0
      else:
        #print('feed item links object has zero length; bozo is fatal')
        pass
    else:
      #print('feed has no links; bozo is fatal')
      return 0
  else:
    #print('could not find feed or channel; bozo is fatal')
    return 0
  # testing shows that there appear to always be entires in the feed
  if 'items' in feedupdate:
    #print('found entries in feed')
    pass
  else:
    #print('feed has no entries; bozo is fatal')
    return 0
  #print('bozo appears to be non-fatal, proceeding to parse feed')
  return 1


def process_feed(feed, data_table):
  name = feed['name']
  url = feed['url']
  tabletime = feed['lastupdate']

  print("Downloading feed for", name)
  feedupdate = feedparser.parse(url)

  if feedupdate.bozo == 1:
    print(name, "produced exception:", feedupdate.bozo_exception, "checking if exception is fatal")
    if check_bozo_feed(feedupdate) == 1:
      process_feed_update(feedupdate, data_table, name)
  else:
    process_feed_update(feedupdate, data_table, name)


#### The actual main part of the program

# Initialize the db connection

db_engine = create_engine(config.db)
Session = sessionmaker(bind=db_engine)
session = Session()
metadata = MetaData()
metadata.reflect(db_engine)

# Make a note in the log
currtime = datetime.now()
#print("Checking RSS feeds for updates at", currtime)
# (Re)load the tables

feed_table = Table('rss_feeds', metadata, autoload_with=db_engine)
data_table = Table('rss_data', metadata, autoload_with=db_engine)

# Get the feeds from the feed table

fq = feed_table.select()
feeds = session.execute(fq)

# Process the feeds from the table

for feed in feeds.mappings():
  process_feed(feed, data_table)

