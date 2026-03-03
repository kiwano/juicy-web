#!/usr/bin/python3

# This program downloads feeds from rss_feeds and adds new items to rss_data
# rss_feeds schema should be: name text, url text, lastupdate timestamp
# rss_data schema should be: name text, update_time timestamp, title text, title_url text, item_title text, item_url text

from time import mktime, sleep
from datetime import datetime, timezone
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from urllib.request import urlopen, urlcleanup
import re
import config


#### Functions


def compare_ymt(first, second):
  if second == None:
    return first
  if first == None:
    return second
  if first['year'] > second['year']:
    return first
  if first['year'] < second['year']:
    return second
  if first['month'] > second['month']:
    return first
  if first['month'] < second['month']:
    return second
  if first['timecode'] > second['timecode']:
    return first
  if first['timecode'] < second['timecode']:
    return second
  return first


### METAR handling functions

def check_metar_record(year, month, station, timecode, url, table):
  tq = table.select().where(
    table.c.station == station).order_by(
    desc(table.c.year)).order_by(
    desc(table.c.month)).order_by(
    desc(table.c.timecode)).limit(1)
  results = session.execute(tq)
  if results.rowcount == 0:
    return True
  for row in results.mappings():
    if row['year'] < year:
      return True
    if row['year'] > year:
      return False
    if row['month'] < month:
      return True
    if row['month'] > month:
      return False
    if row['timecode'] < timecode:
      return True
    if row['timecode'] > timecode:
      return False
  return False


def check_and_update_metar_record(year, month, station, timecode, report, url, table):
  if check_metar_record(year, month, station, timecode, url, table):
    print('Adding new METAR: ' + station + ' ' + str(timecode) + 'Z ' + report)
    iq = table.insert().values(
      station=station,
      timecode=timecode,
      report=report,
      year=year,
      month=month,
      url=url
    )
    session.execute(iq)


def update_metar_station(station_id, station_data, table):
  try:
    urlcleanup()
    f = urlopen(station_data['report'])
  except(Exception, e):
    print('METAR fetch for '+station_id+' failed with exception '+str(e))
    return
  metarlines = f.readlines()
  if len(metarlines) < 2:
    return
  header = metarlines[0].decode(encoding='latin1').strip('\n')
  metar = metarlines[1].decode(encoding='latin1').strip('\n')
  date = header.split(' ')[0]
  try:
    year = int(date.split('/')[0])
    month = int(date.split('/')[1])
  except(Exception, e):
    print('Malformed METAR for '+station_id)
    return
  station = metar.split(' ')[0]
  try:
    timecode = int(metar.split(' ')[1].strip('Z'))
  except(Exception, e):
    print('Malformed METAR for '+station_id)
    return
  report = metar.split(' ', 2)[2]
  check_and_update_metar_record(year, month, station, timecode, report, station_data['target'], table)


def update_metar(stations, table):
  for id in stations.keys():
    update_metar_station(id, stations[id], table)
  session.commit()


### FPCN handling functions

def extract_fpcn_forecast(lines):
  output = lines.pop().decode(encoding='latin1').strip('\n')
  if output == '':
    return output
  while len(lines) != 0:
    nextline = lines.pop().decode(encoding='latin1').strip('\n')
    if nextline == '':
      return output
    if re.match('^ ', nextline):
      output = output + nextline
    else:
      output = output + '\n' + nextline
  return output + ' EOF'


def scan_fpcn(lines, locregex):
  output = ''
  while len(lines) != 0:
    nextline = lines.pop().decode(encoding='latin1').strip('\n')
    if re.match('^End', nextline):
      return output
    if locregex.match(nextline):
      output = extract_fpcn_forecast(lines)
  return output


def select_newest_fpcn(first, second):
  if first['year'] > second['year']:
    return first
  if first['year'] < second['year']:
    return second
  if first['month'] > second['month']:
    return first
  if first['month'] < second['month']:
    return second
  if first['timecode'] > second['timecode']:
    return first
  if first['timecode'] < second['timecode']:
    return second
  if first['text'] == '':
    return second
  return first


def get_new_fpcn(forecast, year, month, day):
  output = {'year': 0, 'month': 1, 'timecode': 0, 'text': ''}
  try:
    f = urlopen(forecast['url'])
  except(Exception, e):
    print('Text forecast fetch for '+forecast['id']+' failed with exception '+str(e))
    return
  fpcnlines = f.read().splitlines()
  fpcnlines.reverse()
  while len(fpcnlines) != 0:
    nextline = fpcnlines.pop().decode(encoding='latin1').strip('\n')
    if forecast['headregex'].match(nextline):
      fpcntime = int(nextline.split(' ')[2])
      forecast_text = scan_fpcn(fpcnlines, forecast['locregex'])
      if forecast_text != '':
        output_candidate = {'year': year, 'month': month, 'timecode': fpcntime, 'text': forecast_text}
        codeday = int(fpcntime/10000)
        if codeday == day:
          output =select_newest_fpcn(output, output_candidate)
        else:
          print("forecast being checked is from yesterday, skipping")
  return output


def get_newest_db_fpcn(table, id):
  tq = table.select().where(
    table.c.fpcn == id).order_by(
    desc(table.c.year)).order_by(
    desc(table.c.month)).order_by(
    desc(table.c.timecode)).limit(1)
  results = session.execute(tq)
  if results.rowcount != 1:
    return None
  for row in results.mappings():
    output = {'year': row['year'], 'month': row['month'], 'timecode': row['timecode'], 'text': row['report']}
  return output


def update_db_fpcn(table, id, data):
  print('updating db with new forecast for '+id)
  iq = table.insert().values(
    fpcn=id,
    timecode=data['timecode'],
    report=data['text'],
    year=data['year'],
    month=data['month'])
  session.execute(iq)


def update_fpcn(fpcns, table, year, month, day):
  for forecast in fpcns.keys():
    fcast_data = get_new_fpcn(fpcns[forecast], year, month, day)
    current_data = get_newest_db_fpcn(table, fpcns[forecast]['id'])
    if compare_ymt(current_data, fcast_data) != current_data:
      update_db_fpcn(table, fpcns[forecast]['id'], fcast_data)
  session.commit()


#### The actual main part of the program

# Initialize the db connection

db_engine = create_engine(config.db)
Session = sessionmaker(bind=db_engine)
session = Session()
metadata = MetaData()
metadata.create_all(db_engine)
metadata.reflect(db_engine)

# Load the tables
metar_table = Table('weather_metar', metadata, autoload_with=db_engine)
fpcn_table = Table('weather_fpcn', metadata, autoload_with=db_engine)

# Get current time and make a note to stdout for logging
currtime = datetime.now()
utctime = datetime.now(timezone.utc)
print("Checking weather resources for updates at", currtime)

# Extract local and UTC year and month information
year = int(currtime.year)
month = int(currtime.month)
day = int(currtime.day)
utcyear = int(utctime.year)
utcmonth = int(utctime.month)
utcday = int(utctime.day)

# Query the METAR and FPCN resources and update the DB as applicable
update_metar(config.metar_stations, metar_table)
update_fpcn(config.fpcn, fpcn_table, year, month, day)
